from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
import cloudinary
import cloudinary.uploader
import os

from app.database.connection import get_database
from app.models.schemas import GalleryFolder, GalleryPhoto

router = APIRouter(prefix="/gallery", tags=["Gallery"])

class CreateFolderRequest(BaseModel):
    folder_name: str
    description: Optional[str] = ""
    is_visible_to_students: bool = True
    cover_image: Optional[str] = ""

class ReorderPhotoRequest(BaseModel):
    photo_ids: List[str]

@router.post("/folders", response_model=GalleryFolder)
async def create_folder(request: CreateFolderRequest, db=Depends(get_database)):
    new_folder = GalleryFolder(
        folder_name=request.folder_name,
        description=request.description,
        is_visible_to_students=request.is_visible_to_students,
        cover_image=request.cover_image,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    doc = new_folder.dict(exclude={"id"})
    doc.pop("_id", None)
    result = await db.gallery_folders.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    doc["id"] = doc["_id"]
    await db.append_audit("CREATE", "GalleryFolder", f"Created folder: {request.folder_name}")
    return doc

@router.get("/folders", response_model=List[GalleryFolder])
async def list_folders(visible_only: bool = False, db=Depends(get_database)):
    query = {"is_visible_to_students": True} if visible_only else {}
    folders = await db.gallery_folders.find(query).to_list(1000)
    for f in folders:
        f["id"] = str(f.get("_id"))
    return folders

@router.put("/folders/{folder_id}", response_model=GalleryFolder)
async def update_folder(folder_id: str, request: CreateFolderRequest, db=Depends(get_database)):
    update_data = {
        "folder_name": request.folder_name,
        "description": request.description,
        "is_visible_to_students": request.is_visible_to_students,
        "updated_at": datetime.utcnow()
    }
    if request.cover_image:
        update_data["cover_image"] = request.cover_image
        
    result = await db.gallery_folders.update_one({"_id": folder_id}, {"$set": update_data})
    if result.matched_count == 0:
        # Might be local JSON DB where IDs are sometimes ints cast to strings, but str(folder_id) should match
        raise HTTPException(status_code=404, detail="Folder not found")
        
    updated = await db.gallery_folders.find_one({"_id": folder_id})
    if updated:
        updated["id"] = str(updated["_id"])
    await db.append_audit("UPDATE", "GalleryFolder", f"Updated folder: {folder_id}")
    return updated

@router.delete("/folders/{folder_id}")
async def delete_folder(folder_id: str, db=Depends(get_database)):
    # Delete the folder
    result = await db.gallery_folders.delete_one({"_id": folder_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Folder not found")
        
    # Delete all associated photos from DB
    photos = await db.gallery_photos.find({"folder_id": folder_id}).to_list(1000)
    for p in photos:
        await db.gallery_photos.delete_one({"_id": p["_id"]})
        # Optional: Delete from cloudinary if we can extract public_id
        # Cloudinary url format: https://res.cloudinary.com/.../upload/v1234/folder/public_id.jpg
        # Since it's complex to extract, and Cloudinary docs recommend keeping it simple, we just delete DB reference.
        
    await db.append_audit("DELETE", "GalleryFolder", f"Deleted folder and its {len(photos)} photos: {folder_id}")
    return {"status": "success", "message": "Folder and photos deleted"}

@router.post("/folders/{folder_id}/photos")
async def upload_photos(
    folder_id: str, 
    files: List[UploadFile] = File(...), 
    db=Depends(get_database)
):
    folder = await db.gallery_folders.find_one({"_id": folder_id})
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    uploaded_photos = []
    for file in files:
        try:
            res = cloudinary.uploader.upload(file.file, folder="gallery")
            new_photo = GalleryPhoto(
                folder_id=folder_id,
                image_url=res.get("secure_url"),
                image_name=file.filename,
                image_size=res.get("bytes", 0),
                display_order=0, # Append at 0
                created_at=datetime.utcnow()
            )
            doc = new_photo.dict(exclude={"id"})
            doc.pop("_id", None)
            result = await db.gallery_photos.insert_one(doc)
            doc["_id"] = str(result.inserted_id)
            doc["id"] = doc["_id"]
            uploaded_photos.append(doc)
            
            # Auto-set cover image if none
            if not folder.get("cover_image"):
                await db.gallery_folders.update_one({"_id": folder_id}, {"$set": {"cover_image": doc["image_url"]}})
                folder["cover_image"] = doc["image_url"]
                
        except Exception as e:
            print(f"Error uploading photo: {e}")
            continue

    await db.append_audit("UPLOAD", "GalleryPhoto", f"Uploaded {len(uploaded_photos)} photos to folder {folder_id}")
    return {"status": "success", "uploaded": uploaded_photos}

@router.get("/folders/{folder_id}/photos", response_model=List[GalleryPhoto])
async def list_photos(folder_id: str, db=Depends(get_database)):
    photos = await db.gallery_photos.find({"folder_id": folder_id}).to_list(1000)
    for p in photos:
        p["id"] = str(p.get("_id"))
    # Sort by display_order, then created_at
    photos.sort(key=lambda x: (x.get("display_order", 0), str(x.get("created_at", ""))))
    return photos

@router.delete("/photos/{photo_id}")
async def delete_photo(photo_id: str, db=Depends(get_database)):
    result = await db.gallery_photos.delete_one({"_id": photo_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Photo not found")
    await db.append_audit("DELETE", "GalleryPhoto", f"Deleted photo: {photo_id}")
    return {"status": "success"}

@router.put("/folders/{folder_id}/cover")
async def set_cover(folder_id: str, image_url: str = Form(...), db=Depends(get_database)):
    result = await db.gallery_folders.update_one({"_id": folder_id}, {"$set": {"cover_image": image_url}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Folder not found")
    return {"status": "success", "cover_image": image_url}

@router.get("/recent")
async def get_recent_photos(limit: int = 10, db=Depends(get_database)):
    # Get visible folders
    folders = await db.gallery_folders.find({"is_visible_to_students": True}).to_list(100)
    visible_folder_ids = [str(f["_id"]) for f in folders]
    
    # Get photos belonging to visible folders
    # Not using complex aggregation here for compatibility with JSON mock DB
    all_photos = []
    for fid in visible_folder_ids:
        photos = await db.gallery_photos.find({"folder_id": fid}).to_list(100)
        # Attach folder name
        folder_name = next((f["folder_name"] for f in folders if str(f["_id"]) == fid), "Gallery")
        for p in photos:
            p["id"] = str(p.get("_id"))
            p["folderName"] = folder_name
            p["title"] = p.get("image_name", "")
            p["url"] = p.get("image_url", "")
            all_photos.append(p)
            
    # Sort by created_at desc
    all_photos.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)
    return all_photos[:limit]

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks, Request
from pydantic import BaseModel
from typing import Optional, Dict, List
import csv
import codecs
from app.database.connection import get_database
from app.models.schemas import Student
from datetime import datetime, timedelta
import random
import urllib.request
import json
import asyncio
import ssl
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
load_dotenv()

# Configure Cloudinary - use CLOUDINARY_URL which auto-configures everything
# CLOUDINARY_URL format: cloudinary://api_key:api_secret@cloud_name
cloudinary_url = os.getenv("CLOUDINARY_URL", "")
if cloudinary_url:
    os.environ["CLOUDINARY_URL"] = cloudinary_url  # ensure it's set for the SDK
import cloudinary.api  # triggers auto-config from CLOUDINARY_URL env var

router = APIRouter()

def send_brevo_email(admin_email: str, student: dict, alert_message: str, risk: str, score: int, emoji: str, date_str: str, time_str: str):
    if not admin_email:
        admin_email = "ulmindsocial.pvtltd@gmail.com"
        
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": os.getenv("BREVO_API_KEY", ""),
        "content-type": "application/json"
    }
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }}
        .header {{ background: linear-gradient(135deg, #ef4444, #dc2626); padding: 30px 20px; text-align: center; color: white; border-bottom: 4px solid #b91c1c; }}
        .header h1 {{ margin: 0; font-size: 24px; letter-spacing: 1px; font-weight: 800; }}
        .content {{ padding: 30px; color: #333333; }}
        .card {{ background: #fff1f2; border-left: 5px solid #ef4444; padding: 20px; margin-bottom: 20px; border-radius: 0 12px 12px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }}
        .card-title {{ margin: 0 0 15px 0; font-size: 13px; color: #9f1239; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 900; }}
        .detail-row {{ margin-bottom: 12px; font-size: 15px; line-height: 1.5; display: flex; }}
        .detail-label {{ font-weight: 800; color: #475569; min-width: 130px; display: inline-block; }}
        .detail-value {{ color: #0f172a; font-weight: 600; flex: 1; }}
        .score-badge {{ display: inline-block; background: #ef4444; color: white; padding: 4px 12px; border-radius: 20px; font-weight: 900; font-size: 14px; box-shadow: 0 2px 4px rgba(239,68,68,0.3); }}
        .footer {{ text-align: center; padding: 25px 20px; color: #64748b; font-size: 12px; background: #f8fafc; border-top: 1px solid #e2e8f0; font-weight: 600; }}
    </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚠️ Student Wellness Alert</h1>
            </div>
            <div class="content">
                <p style="font-size: 16px; color: #475569; margin-top: 0; font-weight: 500; line-height: 1.6; margin-bottom: 25px;">
                    Immediate attention is requested for the following student who checked in with a concerning wellness score.
                </p>
                
                <div class="card">
                    <p class="card-title">Alert Details</p>
                    <div class="detail-row"><span class="detail-label">Message:</span> <span class="detail-value" style="color:#ef4444; font-weight: 800;">{alert_message}</span></div>
                    <div class="detail-row"><span class="detail-label">Risk Level:</span> <span class="detail-value">{risk}</span></div>
                    <div class="detail-row"><span class="detail-label">Score / Mood:</span> <div><span class="score-badge">{score}/10 {emoji}</span></div></div>
                </div>

                <div class="card" style="background: #f0f9ff; border-left: 5px solid #3b82f6;">
                    <p class="card-title" style="color: #1e40af;">Student Information</p>
                    <div class="detail-row"><span class="detail-label">Name:</span> <span class="detail-value">{student.get('firstName', '')} {student.get('lastInitial', '')}</span></div>
                    <div class="detail-row"><span class="detail-label">Roll Number:</span> <span class="detail-value">{student.get('rollNumber', 'Unknown')}</span></div>
                    <div class="detail-row"><span class="detail-label">Class & Sec:</span> <span class="detail-value">{student.get('className', 'Unknown')} - {student.get('section', 'Unknown')}</span></div>
                </div>

                <div class="card" style="background: #fefce8; border-left: 5px solid #eab308;">
                    <p class="card-title" style="color: #a16207;">Timestamp</p>
                    <div class="detail-row"><span class="detail-label">Date:</span> <span class="detail-value">{date_str}</span></div>
                    <div class="detail-row"><span class="detail-label">Time:</span> <span class="detail-value">{time_str}</span></div>
                </div>
                
                <p style="margin-top: 35px; font-size: 14px; color: #64748b; text-align: center; font-weight: 600;">
                    Please log in to the Admin Dashboard to review and resolve this alert.
                </p>
            </div>
            <div class="footer">
                &copy; {date_str[:4]} Kids Attendance System | Premium Automated Alerts
            </div>
        </div>
    </body>
    </html>
    """
    
    data = {
        "sender": {"name": "Kids Attendance Admin", "email": "ulmindsocial.pvtltd@gmail.com"},
        "to": [{"email": admin_email}],
        "subject": f"⚠️ Critical Alert: {student.get('firstName', '')} requires attention",
        "htmlContent": html_content
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method="POST")
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        resp = urllib.request.urlopen(req, timeout=5, context=ctx)
        with open("/tmp/brevo_log.txt", "a") as f:
            f.write("Success: " + resp.read().decode() + "\n")
    except Exception as e:
        error_msg = "Unknown error"
        if hasattr(e, 'read'):
            error_msg = e.read().decode()
        else:
            error_msg = str(e)
        print("Failed to send email via Brevo:")
        print(error_msg)
        with open("/tmp/brevo_log.txt", "a") as f:
            f.write(f"Failed: {error_msg}\n")

# ── In-memory magic-code state (persisted to DB on generate) ──
magic_code_state = {
    "code": "1234",
    "expires_at": datetime.utcnow() + timedelta(hours=8)
}

# ──────────────────────────────────────────────
# Pydantic Models
# ──────────────────────────────────────────────
class LoginRequest(BaseModel):
    roll_number: str
    otp: str

class TeacherLoginRequest(BaseModel):
    username: str
    password: str

class AdminUserRequest(BaseModel):
    username: str
    password: str
    role: Optional[str] = "Teacher"

class WellnessSubmission(BaseModel):
    roll_number: str
    feeling_level: int
    selected_emoji: str
    questions: Dict[str, bool]

# ──────────────────────────────────────────────
# Magic Code
# ──────────────────────────────────────────────
@router.get("/magic-code")
async def get_magic_code():
    return {
        "code": magic_code_state["code"],
        "expires_at": magic_code_state["expires_at"].isoformat()
    }

@router.post("/magic-code/generate")
async def generate_magic_code():
    new_code = f"{random.randint(1000, 9999)}"
    expires_at = datetime.utcnow() + timedelta(hours=8)
    magic_code_state["code"] = new_code
    magic_code_state["expires_at"] = expires_at
    # Audit log
    db = get_database()
    await db.append_audit("GENERATE", "MagicCode", f"New code generated — expires at {expires_at.strftime('%H:%M UTC')}")
    return await get_magic_code()

# ──────────────────────────────────────────────
# Upload — Cloudinary
# ──────────────────────────────────────────────
@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        result = cloudinary.uploader.upload(file.file, folder="students")
        return {"url": result.get("secure_url")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ──────────────────────────────────────────────
# Auth — Student
# ──────────────────────────────────────────────
@router.post("/auth/login")
async def login(request: LoginRequest, db=Depends(get_database)):
    # Verify student exists in DB
    student = await db.students.find_one({"rollNumber": request.roll_number})
    if not student:
        raise HTTPException(status_code=404, detail="Roll number not found in database.")

    # Check unique OTP
    student_otp = student.get("otp", {})
    if not student_otp or student_otp.get("code") != request.otp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OTP")
    # Check unique OTP expiration
    data = await db.get_all_raw()
    settings = data.get("settings", {})
    expiration_hours = settings.get("otp_expiration_hours", 24)
    time_range_enabled = settings.get("otp_time_range_enabled", False)
    start_time_str = settings.get("otp_start_time", "08:00")
    end_time_str = settings.get("otp_end_time", "16:00")
    now = datetime.utcnow()
    
    # Time Range Check
    if time_range_enabled:
        local_now_time = datetime.now().time()
        try:
            start_t = datetime.strptime(start_time_str, "%H:%M").time()
            end_t = datetime.strptime(end_time_str, "%H:%M").time()
            if not (start_t <= local_now_time <= end_t):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"OTP System is only active between {start_time_str} and {end_time_str}")
        except ValueError:
            pass

    is_expired = False
    gen_at_str = student_otp.get("generated_at")
    if gen_at_str:
        try:
            gen_at = datetime.fromisoformat(gen_at_str)
            if (now - gen_at).total_seconds() > (expiration_hours * 3600):
                is_expired = True
        except:
            is_expired = True
    else:
        is_expired = True

    if is_expired:
        # Auto-regenerate on expired login attempt
        code = str(random.randint(1000, 9999))
        new_otp = {"code": code, "used": False, "generated_at": now.isoformat()}
        await db.students.update_one({"rollNumber": request.roll_number}, {"$set": {"otp": new_otp}})
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="OTP has expired. A new one has been generated automatically.")

    await db.append_audit("LOGIN", "Student", f"Student Roll {request.roll_number} logged in with unique OTP", request.roll_number)
    return {"access_token": "mock_token", "token_type": "bearer", "student": {"roll_number": request.roll_number}}

# ──────────────────────────────────────────────
# Auth — Teacher / Admin
# ──────────────────────────────────────────────
@router.post("/auth/teacher-login")
async def teacher_login(request: TeacherLoginRequest, db=Depends(get_database)):
    user = await db.admin_users.find_one({"username": request.username, "password": request.password})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    await db.append_audit("LOGIN", "Admin", f"Admin '{request.username}' logged in", request.username)
    return {"access_token": "teacher_mock_token", "role": user.get("role", "Teacher"), "username": user["username"]}

# ──────────────────────────────────────────────
# Admin User Management
# ──────────────────────────────────────────────
@router.get("/admin-users")
async def get_admin_users(db=Depends(get_database)):
    users = await db.admin_users.find().to_list(100)
    return [{"id": u["_id"], "username": u["username"], "role": u.get("role", "Teacher"), "created_at": u.get("created_at", "")} for u in users]

@router.post("/admin-users")
async def create_admin_user(body: AdminUserRequest, db=Depends(get_database)):
    existing = await db.admin_users.find_one({"username": body.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    now = datetime.utcnow().strftime("%Y-%m-%d")
    await db.admin_users.insert_one({"username": body.username, "password": body.password, "role": body.role, "created_at": now})
    await db.append_audit("CREATE", "AdminUser", f"New admin '{body.username}' (role: {body.role}) added")
    return {"message": "Admin user created successfully"}

@router.delete("/admin-users/{username}")
async def delete_admin_user(username: str, db=Depends(get_database)):
    result = await db.admin_users.delete_one({"username": username})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    await db.append_audit("DELETE", "AdminUser", f"Admin '{username}' removed from system")
    return {"message": f"User '{username}' deleted successfully"}

# ──────────────────────────────────────────────
# Attendance Check
# ──────────────────────────────────────────────
@router.get("/attendance/check/{roll_number}")
async def check_attendance(roll_number: str, db=Depends(get_database)):
    student = await db.students.find_one({"rollNumber": roll_number})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    timeline = student.get("timeline", [])
    today_entry = next((e for e in timeline if e.get("day") == "Today"), None)
    return {
        "already_present": today_entry is not None and today_entry.get("status") != "absent",
        "student_name": f"{student.get('firstName', '')} {student.get('lastInitial', '')}",
        "score": today_entry.get("score") if today_entry else None,
        "emoji": today_entry.get("emoji") if today_entry else None,
    }

# ──────────────────────────────────────────────
# Wellness / Attendance Submission
# ──────────────────────────────────────────────
@router.post("/wellness/submit")
async def submit_wellness(submission: WellnessSubmission, background_tasks: BackgroundTasks, db=Depends(get_database)):
    alert = False
    alert_message = ""
    if submission.feeling_level < 4 or submission.selected_emoji in ["Sad", "Angry", "Sick"]:
        alert = True
        alert_message = "Possible emotional concern"
    for q, ans in submission.questions.items():
        if not ans:
            alert = True
            alert_message = "Wellness score dropped"

    risk = "Stable"
    if submission.feeling_level <= 3:
        risk = "Emotional Drop"
    elif submission.feeling_level <= 5 or alert:
        risk = "Needs Attention"

    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    timeline_entry = {
        "day": "Today",
        "date": today_str,
        "emoji": submission.selected_emoji,
        "score": submission.feeling_level,
        "alert": alert,
        "status": "present",
        "questions": submission.questions
    }

    result = await db.students.update_one(
        {"rollNumber": submission.roll_number},
        {"$push": {"timeline": timeline_entry}, "$set": {"risk": risk}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found in database")

    student = await db.students.find_one({"rollNumber": submission.roll_number})
    # OTP remains active until it naturally expires based on the time configuration.
    
    # Save attendance record
    await db.save_attendance_record({
        "roll_number": submission.roll_number,
        "name": f"{student.get('firstName', '')} {student.get('lastInitial', '')}",
        "status": "present",
        "score": submission.feeling_level,
        "emoji": submission.selected_emoji,
        "risk": risk,
        "alert": alert,
        "date": today_str,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "otp_used": student.get("otp", {}).get("code", "")
    })

    await db.append_audit("ATTENDANCE", "Student",
        f"Roll {submission.roll_number} submitted attendance — score {submission.feeling_level}/10, mood: {submission.selected_emoji}, risk: {risk}",
        submission.roll_number)

    if alert:
        # Fetch admin email setting
        _all = await db.get_all_raw()
        settings_data = _all.get("settings", {})
        admin_email = settings_data.get("admin_notification_email", "ulmindsocial.pvtltd@gmail.com")
        if not admin_email:
            admin_email = "ulmindsocial.pvtltd@gmail.com"
            
        now_dt = datetime.utcnow()
        time_str = now_dt.strftime("%I:%M %p UTC")
        
        background_tasks.add_task(
            send_brevo_email, admin_email, student, alert_message, risk, submission.feeling_level, submission.selected_emoji, today_str, time_str
        )

    return {"status": "success", "alert": alert, "alert_message": alert_message, "risk": risk}

# ──────────────────────────────────────────────
# Notification Settings
# ──────────────────────────────────────────────
@router.get("/settings/notifications")
async def get_notifications(db=Depends(get_database)):
    _all = await db.get_all_raw()
    settings_data = _all.get("settings", {})
    return {"admin_notification_email": settings_data.get("admin_notification_email", "ulmindsocial.pvtltd@gmail.com")}

@router.post("/settings/notifications")
async def save_notifications(data: dict, db=Depends(get_database)):
    raw = await db.get_all_raw()
    if "settings" not in raw:
        raw["settings"] = {}
    raw["settings"]["admin_notification_email"] = data.get("admin_notification_email", "")
    await db.save_raw(raw)
    return {"status": "success"}

# ──────────────────────────────────────────────
# Mark Absent (call at end of school day)
# ──────────────────────────────────────────────
@router.post("/attendance/mark-absent")
async def mark_absent(db=Depends(get_database)):
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    absent_count = await db.mark_absent_students(today_str)
    await db.append_audit("ATTENDANCE", "System", f"End-of-day: {absent_count} student(s) marked absent for {today_str}")
    return {"status": "success", "absent_count": absent_count, "date": today_str}

# ──────────────────────────────────────────────
# Attendance Log & Audit Log
# ──────────────────────────────────────────────
@router.get("/attendance/log")
async def get_attendance_log(db=Depends(get_database)):
    data = await db.get_all_raw()
    return data.get("attendance_log", [])

@router.get("/audit-log")
async def get_audit_log(db=Depends(get_database)):
    return await db.get_audit_log()

# ──────────────────────────────────────────────
# Student CRUD
# ──────────────────────────────────────────────
@router.get("/students/search")
async def search_students(q: str = "", db=Depends(get_database)):
    """Search students by name prefix (case-insensitive). Returns name + roll for autocomplete."""
    if not q or len(q.strip()) < 1:
        return []
    query_lower = q.strip().lower()
    all_students = await db.students.find().to_list(length=1000)
    results = []
    for s in all_students:
        last_initial_full = s.get('lastInitial', '')
        display_last = last_initial_full[0].upper() if last_initial_full else ''
        display_name = f"{s.get('firstName', '')} {display_last}".strip()
        search_target = f"{s.get('firstName', '')} {last_initial_full} {s.get('rollNumber', '')} {s.get('class_name', '')}".lower()
        
        if query_lower in search_target:
            # Get latest emotion from timeline
            timeline = s.get("timeline", [])
            latest_emotion = "⚠️"
            latest_score = 0
            if timeline:
                latest_emotion = timeline[-1].get("emoji", "⚠️")
                latest_score = timeline[-1].get("score", 0)
                
            results.append({
                "id": str(s["_id"]),
                "fullName": display_name,
                "firstName": s.get("firstName", ""),
                "lastInitial": last_initial_full,
                "rollNumber": s.get("rollNumber", ""),
                "className": s.get("class_name", s.get("class", "")),
                "emotion": latest_emotion,
                "emotionScore": latest_score,
                "avatar": s.get("firstName", " ")[0],
                "profilePhoto": s.get("profilePhoto")
            })
    return results[:10]  # max 10 suggestions

@router.get("/students", response_model=List[Student])
async def get_students(db=Depends(get_database)):
    students = await db.students.find().to_list(length=1000)
    for s in students:
        s["_id"] = str(s["_id"])
        s["id"] = s["_id"]
    return students


@router.post("/students", response_model=Student)
async def add_student(student: Student, db=Depends(get_database)):
    existing = await db.students.find_one({"rollNumber": student.rollNumber})
    if existing:
        raise HTTPException(status_code=400, detail="Roll number already exists")
    student_dict = student.dict(exclude={"id"})
    # Remove alias key if present
    student_dict.pop("_id", None)
    student_dict.setdefault("timeline", [])
    student_dict.setdefault("risk", "Stable")
    student_dict.setdefault("attendance", 100)
    student_dict.setdefault("parentStatus", "Pending")
    student_dict.setdefault("status", "active")
    result = await db.students.insert_one(student_dict)
    student_dict["_id"] = str(result.inserted_id)
    student_dict["id"] = student_dict["_id"]
    await db.append_audit("CREATE", "Student",
        f"New student added: {student.firstName} {student.lastInitial} (Roll: {student.rollNumber}, Class: {student.class_name})")
    return student_dict

@router.put("/students/{roll_number}")
async def update_student(roll_number: str, student: Student, db=Depends(get_database)):
    student_dict = student.dict(exclude={"id"}, exclude_unset=True)
    student_dict.pop("_id", None)
    result = await db.students.update_one({"rollNumber": roll_number}, {"$set": student_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    updated = await db.students.find_one({"rollNumber": roll_number})
    updated["_id"] = str(updated["_id"])
    updated["id"] = updated["_id"]
    await db.append_audit("UPDATE", "Student",
        f"Profile updated: {student.firstName} {student.lastInitial} (Roll: {roll_number})")
    return updated

@router.delete("/students/{roll_number}")
async def delete_student(roll_number: str, db=Depends(get_database)):
    student = await db.students.find_one({"rollNumber": roll_number})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    name = f"{student.get('firstName', '')} {student.get('lastInitial', '')}"
    result = await db.students.delete_one({"rollNumber": roll_number})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    await db.append_audit("DELETE", "Student", f"Student removed: {name} (Roll: {roll_number})")
    return {"status": "success", "message": f"Student {name} deleted successfully"}

@router.post("/students/upload_csv")
async def upload_students_csv(file: UploadFile = File(...), db=Depends(get_database)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV.")
    csvReader = csv.DictReader(codecs.iterdecode(file.file, "utf-8"))
    inserted_count = 0
    for row in csvReader:
        if "rollNumber" not in row or "firstName" not in row:
            continue
        student_data = {
            "firstName": row.get("firstName", ""),
            "lastInitial": row.get("lastInitial", ""),
            "rollNumber": row.get("rollNumber", ""),
            "class": row.get("class_name", "Nursery-A"),
            "class_name": row.get("class_name", "Nursery-A"),
            "attendance": 100, "risk": "Stable", "parentStatus": "Pending", "timeline": []
        }
        await db.students.update_one({"rollNumber": student_data["rollNumber"]}, {"$set": student_data}, upsert=True)
        inserted_count += 1
    await db.append_audit("IMPORT", "Students", f"CSV import: {inserted_count} student(s) processed")
    return {"status": "success", "message": f"{inserted_count} students processed."}

# ──────────────────────────────────────────────
# Alerts (existing wellness alerts)
# ──────────────────────────────────────────────
@router.patch("/students/{roll_number}/resolve-alert")
async def resolve_alert(roll_number: str, date: str = "", db=Depends(get_database)):
    student = await db.students.find_one({"rollNumber": roll_number})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    if not date:
        date = datetime.utcnow().strftime("%Y-%m-%d")
        
    # Manually update the timeline entry because mock DB doesn't support $ positional operator
    timeline = student.get("timeline", [])
    updated = False
    for entry in timeline:
        if entry.get("date") == date or entry.get("day") == "Today":
            entry["resolved"] = True
            updated = True
            break
            
    if updated:
        await db.students.update_one({"rollNumber": roll_number}, {"$set": {"timeline": timeline, "risk": "Stable"}})
    else:
        # Also clear the overall student risk status even if not found in timeline
        await db.students.update_one({"rollNumber": roll_number}, {"$set": {"risk": "Stable"}})
        
    name = f"{student.get('firstName', '')} {student.get('lastInitial', '')}"
    await db.append_audit("RESOLVE", "Alert", f"Alert resolved for {name} (Roll: {roll_number}) on {date}")
    return {"status": "success", "message": "Alert resolved", "date": date}

# ──────────────────────────────────────────────
# Student Active/Inactive Toggle
# ──────────────────────────────────────────────
@router.patch("/students/{roll_number}/toggle-status")
async def toggle_student_status(roll_number: str, db=Depends(get_database)):
    student = await db.students.find_one({"rollNumber": roll_number})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    current = student.get("status", "active")
    new_status = "active" if current == "inactive" else "inactive"
    await db.students.update_one({"rollNumber": roll_number}, {"$set": {"status": new_status}})
    name = f"{student.get('firstName', '')} {student.get('lastInitial', '')}"
    await db.append_audit("STATUS", "Student", f"{name} (Roll: {roll_number}) marked {new_status}")
    return {"status": "success", "new_status": new_status}

# ──────────────────────────────────────────────
# Attendance by Date
# ──────────────────────────────────────────────
@router.get("/attendance/by-date")
async def attendance_by_date(date: str = "", db=Depends(get_database)):
    """Get attendance records for a specific date (format: YYYY-MM-DD)."""
    if not date:
        date = datetime.utcnow().strftime("%Y-%m-%d")
    data = await db.get_all_raw()
    logs = data.get("attendance_log", [])
    filtered = [r for r in logs if r.get("date") == date]
    return {"date": date, "records": filtered, "total_present": len(filtered)}

@router.get("/attendance/dates")
async def attendance_dates(db=Depends(get_database)):
    """Get list of all dates that have attendance records."""
    data = await db.get_all_raw()
    logs = data.get("attendance_log", [])
    dates = sorted(list(set(r.get("date", "") for r in logs if r.get("date"))), reverse=True)
    date_counts = {}
    for r in logs:
        d = r.get("date", "")
        if d:
            date_counts[d] = date_counts.get(d, 0) + 1
    return [{"date": d, "count": date_counts.get(d, 0)} for d in dates]

# ──────────────────────────────────────────────
# School Settings
# ──────────────────────────────────────────────
@router.get("/settings/school")
async def get_school_settings(db=Depends(get_database)):
    try:
        if hasattr(db, '_mongo_db') and db._mongo_db is not None:
            doc = await db._mongo_db["school_settings"].find_one({"_id": "school_info"})
            if doc:
                doc.pop("_id", None)
                return doc
            return {}
        else:
            # JSON fallback
            raw = await db.get_all_raw()
            return raw.get("school_settings", {})
    except Exception as e:
        print(f"Error fetching school settings: {e}")
        return {}

@router.post("/settings/school")
async def save_school_settings(request: Request, db=Depends(get_database)):
    data = await request.json()
    try:
        if hasattr(db, '_mongo_db') and db._mongo_db is not None:
            data["_id"] = "school_info"
            await db._mongo_db["school_settings"].replace_one(
                {"_id": "school_info"}, data, upsert=True
            )
            return {"status": "success"}
        else:
            # JSON fallback
            raw = await db.get_all_raw()
            raw["school_settings"] = data
            await db.save_raw(raw)
            return {"status": "success"}
    except Exception as e:
        print(f"Error saving school settings: {e}")
        return {"status": "error", "message": str(e)}

# ──────────────────────────────────────────────
# Classes Management
# ──────────────────────────────────────────────
# ──────────────────────────────────────────────
# Classes & Teachers Management
# ──────────────────────────────────────────────
class ClassItem(BaseModel):
    id: int
    name: str
    section: Optional[str] = ""
    teacher: str
    students: int
    limit: int

class TeacherItem(BaseModel):
    id: int
    name: str
    subject: str
    classes: List[str]

class SchoolDataRequest(BaseModel):
    classes: List[ClassItem]
    teachers: List[TeacherItem]

@router.get("/settings/classes")
async def get_classes(db=Depends(get_database)):
    classes = await db.classes.find().to_list(1000)
    teachers = await db.teachers.find().to_list(1000)
    
    # Format _id to string or map to id
    class_list = []
    for c in classes:
        c["id"] = int(c.get("id", c.get("_id", 0))) if str(c.get("id", c.get("_id", 0))).isdigit() else str(c.get("_id"))
        c.pop("_id", None)
        class_list.append(c)
        
    teacher_list = []
    for t in teachers:
        t["id"] = int(t.get("id", t.get("_id", 0))) if str(t.get("id", t.get("_id", 0))).isdigit() else str(t.get("_id"))
        t.pop("_id", None)
        teacher_list.append(t)
        
    return {
        "classes": class_list if class_list else [
            { "id": 1, "name": "Nursery-A", "teacher": "Emma Watson", "students": 18, "limit": 30 },
            { "id": 2, "name": "Nursery-B", "teacher": "Priya Sharma", "students": 22, "limit": 30 },
            { "id": 3, "name": "KG-A", "teacher": "Anita Roy", "students": 15, "limit": 25 },
        ],
        "teachers": teacher_list if teacher_list else [
            { "id": 1, "name": "Emma Watson", "subject": "Class Teacher", "classes": ["Nursery-A"] },
            { "id": 2, "name": "Priya Sharma", "subject": "Class Teacher", "classes": ["Nursery-B"] },
        ]
    }

@router.post("/settings/classes")
async def save_classes(school_data: SchoolDataRequest, db=Depends(get_database)):
    # Clear existing and insert new ones
    # (A bit inefficient but simplest way to replace the whole list like save_raw did)
    if hasattr(db.classes, 'col'):
        await db.classes.col.delete_many({})
        if school_data.classes:
            await db.classes.col.insert_many([c.dict() for c in school_data.classes])
    else:
        # Mock database fallback
        data = await db.get_all_raw()
        data["classes"] = [c.dict() for c in school_data.classes]
        await db.save_raw(data)
        
    if hasattr(db.teachers, 'col'):
        await db.teachers.col.delete_many({})
        if school_data.teachers:
            await db.teachers.col.insert_many([t.dict() for t in school_data.teachers])
    else:
        data = await db.get_all_raw()
        data["teachers"] = [t.dict() for t in school_data.teachers]
        await db.save_raw(data)

    await db.append_audit("SETTINGS", "Classes & Teachers", "Admin updated the class and teacher lists")
    return {"status": "success"}

from pydantic import BaseModel
from typing import Dict, Any

class ColorSettings(BaseModel):
    clock_emotions: Dict[str, str]
    puzzle_emotions: Dict[str, str]

@router.get("/settings/colors")
async def get_color_settings(db=Depends(get_database)):
    data = await db.get_all_raw()
    return data.get("settings", {
        "clock_emotions": {
            "1": "#6366f1", "2": "#818cf8", "3": "#a78bfa", "4": "#f472b6", "5": "#fb923c",
            "6": "#34d399", "7": "#fbbf24", "8": "#60a5fa", "9": "#a78bfa", "10": "#f9a8d4"
        },
        "puzzle_emotions": {
            "Happy": "#22c55e", "Sad": "#3b82f6", "Mad": "#ef4444", "Scared": "#334155", "Worried": "#eab308", "Excited": "#ec4899"
        }
    })

@router.post("/settings/colors")
async def save_color_settings(settings: ColorSettings, db=Depends(get_database)):
    data = await db.get_all_raw()
    if "settings" not in data:
        data["settings"] = {}
    data["settings"]["clock_emotions"] = settings.clock_emotions
    data["settings"]["puzzle_emotions"] = settings.puzzle_emotions
    await db.save_raw(data)
    await db.append_audit("SETTINGS", "Colors", "Admin updated the emotion color schemes")
    return {"status": "success"}

# ──────────────────────────────────────────────
# Dynamic Emotional Questions Management
# ──────────────────────────────────────────────
class Question(BaseModel):
    id: str
    text: str
    targetType: str  # "global", "class", "student"
    targetValue: Optional[str] = None  # "Class 1 - A" or "Roll 123"
    enabled: bool = True

@router.get("/questions/list")
async def list_questions(db=Depends(get_database)):
    data = await db.get_all_raw()
    questions = data.get("emotional_questions", [
        {"id": "q_sleep", "text": "Did you sleep well last night?", "targetType": "global", "enabled": True},
        {"id": "q_eat", "text": "Did you eat breakfast today?", "targetType": "global", "enabled": True},
        {"id": "q_learn", "text": "Are you excited to learn?", "targetType": "global", "enabled": True},
        {"id": "q_safe", "text": "Are you feeling safe at school?", "targetType": "global", "enabled": True},
        {"id": "q_fun", "text": "Did you have fun yesterday?", "targetType": "global", "enabled": True}
    ])
    # Ensure they exist
    if "emotional_questions" not in data:
        data["emotional_questions"] = questions
        await db.save_raw(data)
    return questions

@router.post("/questions/save")
async def save_questions(req: List[Question], db=Depends(get_database)):
    data = await db.get_all_raw()
    data["emotional_questions"] = [q.dict() for q in req]
    await db.save_raw(data)
    await db.append_audit("SETTINGS", "Questions", f"Admin updated emotional questions. Total active: {len([q for q in req if q.enabled])}")
    return {"status": "success"}

@router.get("/wellness/questions")
async def get_student_questions(rollNumber: str, db=Depends(get_database)):
    student = await db.students.find_one({"rollNumber": rollNumber})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_class = student.get("class", "")
    student_section = student.get("section", "")
    class_str = f"{student_class} - {student_section}"

    data = await db.get_all_raw()
    all_qs = data.get("emotional_questions", [
        {"id": "q_sleep", "text": "Did you sleep well last night?", "targetType": "global", "enabled": True},
        {"id": "q_eat", "text": "Did you eat breakfast today?", "targetType": "global", "enabled": True},
        {"id": "q_learn", "text": "Are you excited to learn?", "targetType": "global", "enabled": True}
    ])

    active_qs = [q for q in all_qs if q.get("enabled")]
    
    # Priority 1: Student Specific
    student_qs = [q for q in active_qs if q.get("targetType") == "student" and q.get("targetValue") == rollNumber]
    
    # Priority 2: Class Specific
    class_qs = [q for q in active_qs if q.get("targetType") == "class" and q.get("targetValue") == class_str]
    
    # Priority 3: Global
    global_qs = [q for q in active_qs if q.get("targetType") == "global"]

    # Select exactly 3
    selected = student_qs.copy()
    if len(selected) < 3:
        # Fill with class qs
        needed = 3 - len(selected)
        import random
        random.shuffle(class_qs)
        selected.extend(class_qs[:needed])
        
    if len(selected) < 3:
        # Fill with global
        needed = 3 - len(selected)
        import random
        random.shuffle(global_qs)
        # Prevent duplicates
        existing_texts = {q.get("text") for q in selected}
        available_global = [q for q in global_qs if q.get("text") not in existing_texts]
        selected.extend(available_global[:needed])

    # Trim to 3 if somehow more
    selected = selected[:3]
    return selected

@router.get("/questions/history")
async def get_questions_history(db=Depends(get_database)):
    data = await db.get_all_raw()
    students = data.get("students", [])
    
    history = []
    # Parse timeline from all students
    for s in students:
        timeline = s.get("timeline", [])
        student_name = f"{s.get('firstName', '')} {s.get('lastInitial', '')}"
        roll = s.get("rollNumber")
        
        for entry in timeline:
            if "questions" in entry and entry["questions"]:
                history.append({
                    "date": entry.get("date"),
                    "studentName": student_name,
                    "rollNumber": roll,
                    "questions": entry["questions"],
                    "score": entry.get("score"),
                    "emoji": entry.get("emoji")
                })
                
    # Sort by date descending
    history.sort(key=lambda x: x["date"], reverse=True)
    return history

class GenerateOTPRequest(BaseModel):
    action: str  # "class", "student", "all"
    class_name: Optional[str] = None
    section_name: Optional[str] = None
    roll_number: Optional[str] = None
    custom_otp: Optional[str] = None

class OTPConfigRequest(BaseModel):
    expiration_hours: int
    time_range_enabled: Optional[bool] = False
    start_time: Optional[str] = "08:00"
    end_time: Optional[str] = "16:00"

@router.get("/settings/otp-config")
async def get_otp_config(db=Depends(get_database)):
    data = await db.get_all_raw()
    settings = data.get("settings", {})
    return {
        "expiration_hours": settings.get("otp_expiration_hours", 24),
        "time_range_enabled": settings.get("otp_time_range_enabled", False),
        "start_time": settings.get("otp_start_time", "08:00"),
        "end_time": settings.get("otp_end_time", "16:00")
    }

@router.post("/settings/otp-config")
async def save_otp_config(req: OTPConfigRequest, db=Depends(get_database)):
    data = await db.get_all_raw()
    if "settings" not in data:
        data["settings"] = {}
    data["settings"]["otp_expiration_hours"] = req.expiration_hours
    data["settings"]["otp_time_range_enabled"] = req.time_range_enabled
    data["settings"]["otp_start_time"] = req.start_time
    data["settings"]["otp_end_time"] = req.end_time
    await db.save_raw(data)
    await db.append_audit("SETTINGS", "OTP", f"Admin updated OTP settings")
    return {"status": "success"}

@router.get("/otps/list")
async def list_otps(db=Depends(get_database)):
    data = await db.get_all_raw()
    expiration_hours = data.get("settings", {}).get("otp_expiration_hours", 24)
    now = datetime.utcnow()
    
    students = await db.students.find().to_list(1000)
    result = []
    for s in students:
        otp_data = s.get("otp", {})
        
        # Check expiration and auto-regenerate if needed
        is_expired = False
        gen_at_str = otp_data.get("generated_at")
        if gen_at_str:
            try:
                gen_at = datetime.fromisoformat(gen_at_str)
                if (now - gen_at).total_seconds() > (expiration_hours * 3600):
                    is_expired = True
            except:
                is_expired = True
        else:
            is_expired = True
            
        if is_expired:
            code = str(random.randint(1000, 9999))
            otp_data = {"code": code, "used": False, "generated_at": now.isoformat()}
            await db.students.update_one({"rollNumber": s["rollNumber"]}, {"$set": {"otp": otp_data}})
            
        result.append({
            "rollNumber": s["rollNumber"],
            "name": f"{s.get('firstName', '')} {s.get('lastInitial', '')}",
            "className": s.get("class_name", s.get("class", "Nursery")),
            "section": s.get("section", "A"),
            "otp": otp_data,
            "profilePhoto": s.get("profilePhoto"),
            "initial": s.get("firstName", " ")[0] if s.get("firstName") else ""
        })
    return result

@router.post("/otps/generate")
async def generate_otps(req: GenerateOTPRequest, db=Depends(get_database)):
    students = await db.students.find().to_list(1000)
    updated_count = 0
    
    for s in students:
        should_update = False
        if req.action == "all":
            should_update = True
        elif req.action == "class" and s.get("class_name", s.get("class")) == req.class_name and s.get("section") == req.section_name:
            should_update = True
        elif req.action == "student" and s.get("rollNumber") == req.roll_number:
            should_update = True
            
        if should_update:
            code = req.custom_otp if (req.action == "student" and req.custom_otp) else str(random.randint(1000, 9999))
            new_otp = {"code": code, "used": False, "generated_at": datetime.utcnow().isoformat()}
            await db.students.update_one({"rollNumber": s["rollNumber"]}, {"$set": {"otp": new_otp}})
            updated_count += 1
            
    await db.append_audit("GENERATE", "OTP", f"Generated {updated_count} new unique OTPs (Action: {req.action})")
    return {"status": "success", "updated": updated_count}

@router.get("/otps/history")
async def get_otp_history(db=Depends(get_database)):
    data = await db.get_all_raw()
    logs = data.get("attendance_log", [])
    
    # Pre-fetch students to map class and name robustly
    students = await db.students.find().to_list(1000)
    student_map = {s.get("rollNumber"): s for s in students}
    
    history = []
    for log in logs:
        if log.get("otp_used"):
            roll = log.get("roll_number")
            s = student_map.get(roll, {})
            name = log.get("name") or log.get("student_name") or f"{s.get('firstName', '')} {s.get('lastInitial', '')}".strip() or "Unknown Student"
            student_class = s.get("class", s.get("class_name", "Unknown Class"))
            
            history.append({
                "date": log.get("date"),
                "time": log.get("timestamp"),
                "rollNumber": roll,
                "studentName": name,
                "className": student_class,
                "otp": log.get("otp_used")
            })
    # Sort by timestamp descending
    history.sort(key=lambda x: x["time"], reverse=True)
    return history

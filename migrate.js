
// Run this in MongoDB Atlas Data Explorer or mongosh
use kids_attendance;
db.students.deleteMany({});
db.students.insertMany([
  {
    "firstName": "Deepsundar",
    "lastInitial": "Das",
    "rollNumber": "181",
    "class": "Nursery-A",
    "class_name": "Nursery-A",
    "section": "A",
    "attendance": 100,
    "risk": "Stable",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-15",
        "emoji": "Happy",
        "score": 3,
        "alert": true,
        "status": "present",
        "questions": {
          "sleep": true,
          "safe": false,
          "breakfast": true
        },
        "resolved": true
      }
    ],
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "status": "active",
    "otp": {
      "code": "4456",
      "used": false,
      "generated_at": "2026-05-17T06:17:36.749428"
    }
  },
  {
    "firstName": "Aditya",
    "lastInitial": "Kumar",
    "rollNumber": "182",
    "class": "Nursery-A",
    "class_name": "Nursery-A",
    "section": "A",
    "attendance": 100,
    "risk": "Stable",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-15",
        "emoji": "Sad",
        "score": 10,
        "alert": true,
        "status": "present",
        "questions": {
          "sleep": true,
          "safe": true,
          "breakfast": true
        },
        "resolved": true
      }
    ],
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "status": "active",
    "otp": {
      "code": "3285",
      "used": false,
      "generated_at": "2026-05-16T16:25:19.378060"
    }
  },
  {
    "firstName": "Ratnadip",
    "lastInitial": "Shit",
    "rollNumber": "183",
    "class": "Nursery-A",
    "class_name": "Nursery-A",
    "section": "A",
    "attendance": 100,
    "risk": "Needs Attention",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-15",
        "emoji": "Happy",
        "score": 7,
        "alert": true,
        "status": "present",
        "questions": {
          "sleep": true,
          "safe": true,
          "breakfast": false
        }
      }
    ],
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "status": "inactive",
    "otp": {
      "code": "2387",
      "used": false,
      "generated_at": "2026-05-16T16:25:19.378060"
    }
  },
  {
    "firstName": "Samiran",
    "lastInitial": "S",
    "rollNumber": "185",
    "class": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Stable",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-15",
        "emoji": "Sad",
        "score": 7,
        "alert": true,
        "status": "present",
        "questions": {
          "sleep": true,
          "safe": true,
          "breakfast": false
        },
        "resolved": true
      }
    ],
    "otp": {
      "code": "3334",
      "used": false,
      "generated_at": "2026-05-16T16:25:19.378060"
    }
  },
  {
    "firstName": "Arnab",
    "lastInitial": "S",
    "rollNumber": "189",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Needs Attention",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-16",
        "emoji": "Happy",
        "score": 5,
        "alert": true,
        "status": "present",
        "questions": {
          "sleep": false,
          "safe": true,
          "breakfast": true
        }
      }
    ],
    "status": "active",
    "class": "LKG",
    "otp": {
      "code": "4677",
      "used": false,
      "generated_at": "2026-05-16T15:39:22.085260"
    }
  },
  {
    "firstName": "Samiran",
    "lastInitial": "J",
    "rollNumber": "190",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Needs Attention",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-16",
        "emoji": "Excited",
        "score": 5,
        "alert": true,
        "status": "present",
        "questions": {
          "Do you miss home?": true,
          "Are you ready to learn?": true,
          "Are you feeling good?": false
        }
      }
    ],
    "status": "active",
    "class": "UKG",
    "otp": {
      "code": "9671",
      "used": false,
      "generated_at": "2026-05-17T14:19:01.147560"
    }
  },
  {
    "firstName": "Dipan",
    "lastInitial": "J",
    "rollNumber": "178",
    "class_name": "Nursery-B",
    "section": "B",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Stable",
    "parentStatus": "Pending",
    "timeline": [],
    "status": "inactive",
    "class": "UKG",
    "otp": {
      "code": "2939",
      "used": false,
      "generated_at": "2026-05-16T16:25:19.378060"
    }
  },
  {
    "firstName": "Roni",
    "lastInitial": "F",
    "rollNumber": "167",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Stable",
    "parentStatus": "Pending",
    "timeline": [],
    "status": "active",
    "class": "UKG",
    "otp": {
      "code": "3866",
      "used": false,
      "generated_at": "2026-05-16T16:25:19.378060"
    }
  },
  {
    "firstName": "Shiva",
    "lastInitial": "G",
    "rollNumber": "251",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Needs Attention",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-16",
        "emoji": "Happy",
        "score": 5,
        "alert": true,
        "status": "present",
        "questions": {
          "Are you feeling good?": true,
          "Do you miss home?": true,
          "Did someone make you smile?": false
        }
      }
    ],
    "status": "active",
    "class": "LKG",
    "otp": {
      "code": "6221",
      "used": false,
      "generated_at": "2026-05-16T16:25:19.378060"
    }
  },
  {
    "firstName": "Bardhaman",
    "lastInitial": "L",
    "rollNumber": "199",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Stable",
    "parentStatus": "Pending",
    "timeline": [],
    "status": "active",
    "class": "Class 1",
    "otp": {
      "code": "2982",
      "used": false,
      "generated_at": "2026-05-16T16:25:19.378060"
    }
  },
  {
    "firstName": "Soumyajit",
    "lastInitial": "B",
    "rollNumber": "367",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Stable",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-16",
        "emoji": "Sad",
        "score": 2,
        "alert": true,
        "status": "present",
        "questions": {
          "Did someone make you smile?": true,
          "Are you feeling good?": false,
          "Are you ready to learn?": true
        },
        "resolved": true
      }
    ],
    "status": "active",
    "otp": {
      "code": "3142",
      "used": false,
      "generated_at": "2026-05-16T19:08:01.657548"
    }
  },
  {
    "firstName": "Arnab",
    "lastInitial": "K",
    "rollNumber": "678",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Stable",
    "parentStatus": "Pending",
    "timeline": [],
    "status": "active",
    "otp": {
      "code": "3735",
      "used": false,
      "generated_at": "2026-05-16T19:13:12.073895"
    }
  },
  {
    "firstName": "Samiran",
    "lastInitial": "K",
    "rollNumber": "898",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Needs Attention",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-16",
        "emoji": "Excited",
        "score": 10,
        "alert": true,
        "status": "present",
        "questions": {
          "Did someone make you smile?": true,
          "Are you feeling good?": true,
          "Do you miss home?": false
        }
      }
    ],
    "status": "active",
    "otp": {
      "code": "5604",
      "used": false,
      "generated_at": "2026-05-17T14:18:48.879479"
    }
  },
  {
    "firstName": "Arnab",
    "lastInitial": "Das",
    "rollNumber": "784",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Emotional Drop",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-17",
        "emoji": "Worried",
        "score": 2,
        "alert": true,
        "status": "present",
        "questions": {
          "Are you feeling good?": true,
          "Did someone make you smile?": true,
          "Do you miss home?": false
        }
      }
    ],
    "status": "active",
    "otp": {
      "code": "3265",
      "used": false,
      "generated_at": "2026-05-17T14:18:49.459148"
    }
  },
  {
    "firstName": "Tirtha",
    "lastInitial": "L",
    "rollNumber": "927",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Emotional Drop",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-17",
        "emoji": "Sad",
        "score": 2,
        "alert": true,
        "status": "present",
        "questions": {
          "Are you ready to learn?": true,
          "Did someone make you smile?": true,
          "Do you miss home?": false
        }
      }
    ],
    "status": "active",
    "otp": {
      "code": "3838",
      "used": false,
      "generated_at": "2026-05-17T14:18:50.399947"
    }
  },
  {
    "firstName": "Amir",
    "lastInitial": "K",
    "rollNumber": "577",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Emotional Drop",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-17",
        "emoji": "Worried",
        "score": 2,
        "alert": true,
        "status": "present",
        "questions": {
          "Are you ready to learn?": false,
          "Did someone make you smile?": false,
          "Do you miss home?": true
        }
      }
    ],
    "status": "active",
    "otp": {
      "code": "7688",
      "used": false,
      "generated_at": "2026-05-17T14:18:50.964326"
    }
  },
  {
    "firstName": "Sourav",
    "lastInitial": "K",
    "rollNumber": "579",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Emotional Drop",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-17",
        "emoji": "Sad",
        "score": 2,
        "alert": true,
        "status": "present",
        "questions": {
          "Did someone make you smile?": false,
          "Are you feeling good?": false,
          "Do you miss home?": false
        }
      }
    ],
    "status": "active",
    "otp": {
      "code": "8461",
      "used": false,
      "generated_at": "2026-05-17T14:18:51.450330"
    }
  },
  {
    "firstName": "Amir",
    "lastInitial": "K",
    "rollNumber": "388",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Emotional Drop",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-17",
        "emoji": "Sad",
        "score": 2,
        "alert": true,
        "status": "present",
        "questions": {
          "Are you ready to learn?": false,
          "Are you feeling good?": false,
          "Do you miss home?": false
        }
      },
      {
        "day": "Today",
        "date": "2026-05-17",
        "emoji": "Sad",
        "score": 2,
        "alert": true,
        "status": "present",
        "questions": {}
      },
      {
        "day": "Today",
        "date": "2026-05-17",
        "emoji": "Sad",
        "score": 2,
        "alert": true,
        "status": "present",
        "questions": {}
      },
      {
        "day": "Today",
        "date": "2026-05-17",
        "emoji": "Sad",
        "score": 2,
        "alert": true,
        "status": "present",
        "questions": {}
      },
      {
        "day": "Today",
        "date": "2026-05-17",
        "emoji": "Sad",
        "score": 2,
        "alert": true,
        "status": "present",
        "questions": {}
      },
      {
        "day": "Today",
        "date": "2026-05-17",
        "emoji": "Sad",
        "score": 2,
        "alert": true,
        "status": "present",
        "questions": {}
      }
    ],
    "status": "active",
    "otp": {
      "code": "8759",
      "used": false,
      "generated_at": "2026-05-17T14:18:51.981338"
    }
  },
  {
    "firstName": "Sagnik",
    "lastInitial": "Mu",
    "rollNumber": "926",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Emotional Drop",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-17",
        "emoji": "Sad",
        "score": 2,
        "alert": true,
        "status": "present",
        "questions": {
          "Are you ready to learn?": true,
          "Do you miss home?": false,
          "Are you feeling good?": false
        }
      }
    ],
    "status": "active",
    "otp": {
      "code": "9389",
      "used": false,
      "generated_at": "2026-05-17T14:18:52.514953"
    }
  },
  {
    "firstName": "Ram",
    "lastInitial": "K",
    "rollNumber": "772",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Emotional Drop",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-17",
        "emoji": "Sad",
        "score": 2,
        "alert": true,
        "status": "present",
        "questions": {
          "Are you feeling good?": false,
          "Are you ready to learn?": false,
          "Do you miss home?": false
        }
      }
    ],
    "status": "active",
    "otp": {
      "code": "5579",
      "used": false,
      "generated_at": "2026-05-17T14:18:52.999266"
    }
  },
  {
    "firstName": "Abir",
    "lastInitial": "C",
    "rollNumber": "499",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Emotional Drop",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-17",
        "emoji": "Sad",
        "score": 2,
        "alert": true,
        "status": "present",
        "questions": {
          "Do you miss home?": false,
          "Are you feeling good?": false,
          "Are you ready to learn?": false
        }
      }
    ],
    "status": "active",
    "otp": {
      "code": "1199",
      "used": false,
      "generated_at": "2026-05-17T14:18:54.581673"
    }
  },
  {
    "firstName": "Syam",
    "lastInitial": "K",
    "rollNumber": "278",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Needs Attention",
    "parentStatus": "Pending",
    "timeline": [
      {
        "day": "Today",
        "date": "2026-05-17",
        "emoji": "Sad",
        "score": 5,
        "alert": true,
        "status": "present",
        "questions": {
          "Do you miss home?": true,
          "Are you feeling good?": true,
          "Did someone make you smile?": true
        }
      }
    ],
    "status": "active",
    "otp": {
      "code": "9245",
      "used": false,
      "generated_at": "2026-05-17T14:18:05.565389"
    }
  },
  {
    "firstName": "Arnab",
    "lastInitial": "S",
    "rollNumber": "254",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "",
    "attendance": 100,
    "risk": "Stable",
    "parentStatus": "Pending",
    "timeline": [],
    "status": "active",
    "otp": {
      "code": "5973",
      "used": false,
      "generated_at": "2026-05-17T16:10:40.289163"
    }
  },
  {
    "firstName": "Arnab",
    "lastInitial": "J",
    "rollNumber": "479",
    "class_name": "Nursery-A",
    "section": "A",
    "parentsName": "",
    "parentsPhone": "",
    "bloodGroup": "",
    "profilePhoto": "https://res.cloudinary.com/dmeu6hdwg/image/upload/v1779033788/dnquu57dwkmonnmdupkf.jpg",
    "attendance": 100,
    "risk": "Stable",
    "parentStatus": "Pending",
    "timeline": [],
    "status": "active",
    "otp": {
      "code": "5554",
      "used": false,
      "generated_at": "2026-05-17T16:10:40.289163"
    }
  }
]);
print('Inserted ' + db.students.countDocuments({}) + ' students');

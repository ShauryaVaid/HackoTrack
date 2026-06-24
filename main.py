from fastapi import FastAPI, Path, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
import os
from dotenv import load_dotenv
from Mysql_db import fetch_all_users, insert_user, get_user_id_by_email
from pydantic import BaseModel, Field
from typing import Annotated, Optional, List
import random
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ADMIN_API_KEY = os.getenv("ADMIN_PASS", "HCKTRK26")
api_key_header = APIKeyHeader(name="X-Admin-Key", auto_error=True)

async def get_admin_key(api_key: str = Security(api_key_header)):
    if api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

class HackathonBase(BaseModel):
    user_name: Annotated[str, Field(..., description='Name of the user', examples=['Shaurya Vaid'])]
    user_email: Annotated[str, Field(..., description='Email of the user', examples=['user@example.com'])]
    linkedin_url: Annotated[Optional[str], Field(default=None, description='LinkedIn URL', examples=['https://linkedin.com/in/user'])]
    github_url: Annotated[Optional[str], Field(default=None, description='GitHub URL', examples=['https://github.com/user'])]
    hackathon_name: Annotated[str, Field(..., description='Hackathon name', examples=['TechHack2024'])]
    organizing_community: Annotated[Optional[str], Field(default=None, description='Organizing community', examples=['DevCommunity'])]
    application_date: Annotated[str, Field(..., description='Application date', examples=['2024-01-15'])]
    rough_start_month: Annotated[Optional[str], Field(default=None, description='Rough start month', examples=['January'])]
    tentative_start_date: Annotated[Optional[str], Field(default=None, description='Tentative start date', examples=['2024-02-01'])]
    created_at: Annotated[Optional[str], Field(default=None, description='Creation timestamp', examples=['2024-01-15T10:30:00'])]
    description: Annotated[Optional[str], Field(default=None, description='Hackathon description')]
    location: Annotated[Optional[str], Field(default=None, description='Location')]
    tags: Annotated[Optional[str], Field(default=None, description='Tags')]
    tech_stack: Annotated[Optional[str], Field(default=None, description='Tech stack')]
    prize_pool: Annotated[Optional[str], Field(default=None, description='Prize pool')]
    team_size: Annotated[Optional[str], Field(default=None, description='Team size')]
    rules: Annotated[Optional[str], Field(default=None, description='Rules')]
    registration_link: Annotated[Optional[str], Field(default=None, description='Registration link')]
    venue_details: Annotated[Optional[str], Field(default=None, description='Venue details')]

class HackathonCreate(HackathonBase):
    pass

class HackathonUpdate(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    hackathon_name: Optional[str] = None
    organizing_community: Optional[str] = None
    application_date: Optional[str] = None
    rough_start_month: Optional[str] = None
    tentative_start_date: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    tags: Optional[str] = None
    tech_stack: Optional[str] = None
    prize_pool: Optional[str] = None
    team_size: Optional[str] = None
    rules: Optional[str] = None
    registration_link: Optional[str] = None
    venue_details: Optional[str] = None

class HackathonResponse(HackathonBase):
    entry_id: Annotated[int, Field(..., description='Id of the hackathon post', examples=[1001])]
    user_id: Annotated[int, Field(..., description='User ID', examples=[1])]

load_dotenv()


def load_data():
    pass

@app.get("/")
def hello():
    return {'message': 'HackoTrack System API'}


@app.get("/about")
def about():
    return {'message': 'This doesnt miss deadlines as its managed by and for the student!'}


@app.get("/hackathons/columns")
def get_hackathon_columns():
    return {
        'columns': [
            {'name': 'entry_id', 'description': 'Id of the hackathon entry', 'example': '1001'},
            {'name': 'user_id', 'description': 'User ID', 'example': '1'},
            {'name': 'user_name', 'description': 'Name of the user', 'example': 'Shaurya Vaid'},
            {'name': 'user_email', 'description': 'Email of the user', 'example': 'user@example.com'},
            {'name': 'linkedin_url', 'description': 'LinkedIn URL', 'example': 'https://linkedin.com/in/user'},
            {'name': 'github_url', 'description': 'GitHub URL', 'example': 'https://github.com/user'},
            {'name': 'hackathon_name', 'description': 'Hackathon name', 'example': 'TechHack2024'},
            {'name': 'organizing_community', 'description': 'Organizing community', 'example': 'DevCommunity'},
            {'name': 'application_date', 'description': 'Application date', 'example': '2024-01-15'},
            {'name': 'rough_start_month', 'description': 'Rough start month', 'example': 'January'},
            {'name': 'tentative_start_date', 'description': 'Tentative start date', 'example': '2024-02-01'},
            {'name': 'created_at', 'description': 'Creation timestamp', 'example': '2024-01-15T10:30:00'},
        ]
    }


@app.get("/hackathons", response_model=List[HackathonResponse])
def get_all_hackathons():
    data = fetch_all_users()
    if not data:
        return []
    return data


@app.get("/hackathons/search", response_model=List[HackathonResponse])
def search_hackathons(q: str = Query(..., description='Search by hackathon name or user name')):
    data = fetch_all_users()
    if not data:
        return []

    results = []
    q_lower = q.lower()
    for item in data:
        h_name = str(item.get('hackathon_name') or '')
        u_name = str(item.get('user_name') or '')
        if q_lower in h_name.lower() or q_lower in u_name.lower():
            results.append(item)
            
    return results


@app.post("/hackathons")
def create_hackathon(hackathon: HackathonCreate):
    try:
        data = hackathon.model_dump()
        
        # Map user_id smartly by checking if email already exists
        existing_user_id = get_user_id_by_email(data['user_email'])
        if existing_user_id:
            data['user_id'] = existing_user_id
        else:
            data['user_id'] = random.randint(1000, 9999)
            
        # Entry ID is always unique per hackathon post
        data['entry_id'] = random.randint(10000, 99999)
            
        result = insert_user(data)
        return {
            'message': 'Hackathon added successfully', 
            'data': result, 
            'entry_id': data['entry_id'], 
            'user_id': data['user_id']
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from Mysql_db import delete_hackathon, update_hackathon

@app.delete("/hackathons/{entry_id}")
def delete_hackathon_endpoint(entry_id: int, api_key: str = Depends(get_admin_key)):
    try:
        success = delete_hackathon(entry_id)
        if success:
            return {"message": "Hackathon deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Hackathon not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/hackathons/{entry_id}")
def update_hackathon_endpoint(entry_id: int, hackathon: HackathonUpdate, api_key: str = Depends(get_admin_key)):
    try:
        data = hackathon.model_dump(exclude_unset=True)
        success = update_hackathon(entry_id, data)
        if success:
            return {"message": "Hackathon updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Hackathon not found or no changes made")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

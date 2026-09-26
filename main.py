from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#rag
# import embedding

# file router import 
from Registration import router as registration_router
from Transation import router as transation_router
from support import router as support_router
from user_profile import router as profile_router
from groq_service import router as groq_router


app = FastAPI()

app.include_router(registration_router)
app.include_router(transation_router)
app.include_router(support_router)
app.include_router(profile_router)
app.include_router(groq_router)



app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)
    
@app.get("/")
def app_health():
    return {
        "status": "healthy",
        "message": "Secure Bank backend running"
        }
        

       
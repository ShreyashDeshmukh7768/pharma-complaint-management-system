from app.api.routes.upload import router as upload_router
from app.api.routes.complaint import router as complaint_router

__all__ = [
    "complaint_router",
    "upload_router",
]
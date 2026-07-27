"""CRUD package exports."""

from app.crud.complaint import (
	create_complaint,
	delete_complaint,
	get_all_complaints,
	get_complaint_by_id,
	get_complaint_by_number,
    get_latest_complaint,
	update_complaint,
)

__all__ = [
	"create_complaint",
	"get_complaint_by_id",
	"get_complaint_by_number",
	"get_all_complaints",
	"update_complaint",
	"delete_complaint",
    "get_latest_complaint",
]


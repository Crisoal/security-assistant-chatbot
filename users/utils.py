# users/utils.py
from django.db.models import Q
from django.utils import timezone

def get_user_progress_percentage(user):
    # Calculate progress based on completed security modules
    # Replace this with your actual progress calculation logic
    if user.role == 'business_owner':
        # Business owners have different modules
        completed_modules = user.businessownertraining_set.filter(completed=True).count()
        total_modules = user.businessownertraining_set.count() or 1
    elif user.role == 'employee':
        completed_modules = user.employeetraining_set.filter(completed=True).count()
        total_modules = user.employeetraining_set.count() or 1
    else:
        completed_modules = user.technicalstafftraining_set.filter(completed=True).count()
        total_modules = user.technicalstafftraining_set.count() or 1
        
    return int((completed_modules / total_modules * 100) if total_modules > 0 else 0)

def update_user_progress(user, module_completed):
    """Update user's progress when they complete a module"""
    if user.role == 'business_owner':
        user.businessownertraining_set.filter(id=module_completed.id).update(
            completed=True,
            completed_at=timezone.now()
        )
    elif user.role == 'employee':
        user.employeetraining_set.filter(id=module_completed.id).update(
            completed=True,
            completed_at=timezone.now()
        )
    else:
        user.technicalstafftraining_set.filter(id=module_completed.id).update(
            completed=True,
            completed_at=timezone.now()
        )
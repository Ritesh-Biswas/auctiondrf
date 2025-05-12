from django.db.models.signals import post_migrate, post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.db import transaction

@receiver(post_migrate)
def create_default_users_and_groups(sender, **kwargs):
    try:
        with transaction.atomic():
            # Create superuser if it doesn't exist
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    password='admin@123',
                    email='admin@example.com'
                )
                print("Superuser created successfully!")

            # Create groups if they don't exist
            groups = ['MP_Admin', 'SA_Admin', 'Sellers', 'Users']
            for group_name in groups:
                Group.objects.get_or_create(name=group_name)
                print(f"Group '{group_name}' created successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    if created and not instance.groups.exists() and not instance.is_superuser:
        default_group = Group.objects.get(name='Users')
        instance.groups.add(default_group)
        print(f"User {instance.username} added to Users group")

@receiver(m2m_changed, sender=User.groups.through)
def update_staff_status(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        if instance.groups.filter(name='MP_Admin').exists():
            instance.is_staff = True
            instance.save()
            print(f"User {instance.username} staff status updated to True")
    elif action == "post_remove":
        if not instance.groups.filter(name='MP_Admin').exists():
            instance.is_staff = False
            instance.save()
            print(f"User {instance.username} staff status updated to False")

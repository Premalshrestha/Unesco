from django.core.management.base import BaseCommand
from myapp.models import Category

class Command(BaseCommand):
    help = 'Create initial discussion categories'
    
    def handle(self, *args, **options):
        categories = [
            {
                'name': 'General Discussion',
                'slug': 'general',
                'description': 'General topics and open discussions'
            },
            
            
            {
                'name': 'Mental Health',
                'slug': 'mental-health',
                'description': 'Mental health support and discussions'
            },
            
            
            {
                'name': 'Career Advice',
                'slug': 'career-advice',
                'description': 'Career guidance and professional development'
            },
            {
                'name': 'Health & Wellness',
                'slug': 'health-wellness',
                'description': 'Health, fitness, and wellness discussions'
            },
            
            
            {
                'name': 'Pregnancy',
                'slug': 'pregnancy',
                'description': 'Learning resources and educational discussions'
            }
        ]
        
        created_count = 0
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(f'Category already exists: {category.name}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new categories!')
        )
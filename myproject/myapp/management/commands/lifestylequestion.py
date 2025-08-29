from django.core.management.base import BaseCommand
from myapp.models import LifestyleQuestion


class Command(BaseCommand):
    help="loading the uestions of lifestyle misconception in the dtaabase"

    #this function tells to handle if extra parameter is passed
    def handle(self, *args, **options):
        sample_questions= [
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },
        {
            'question_text':"how are you?",
            'option_a':'I am fine',
            'option_b':'I am not fine',
            'option_c':'I feel good',
            'option_d':'I am tired',
            'correct_answer':'I am not fine',
            'explanation':"my day was good what"
        },

        ]

        created_count=0

#this helps to loop thorugh the sample question create object in database
        for question_data in sample_questions:
            question, created=LifestyleQuestion.objects.get_or_create (
                #this helps to prevent the duplicate data

                #harek choti hamro database ma vako question_text ma sample question bata mathi ko euta lop ma question_data halxa 
                #aani get or create le check garxa xaina vane duplicate huna dinna aani question add garxa
                question_text= question_data['question_text'],
                defaults=question_data
            )
            
            #tya get or create gareko xa tesko matlab ki data banaue ki naya create garney
            if created:
                created_count +=1
        

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded {created_count} new questions. Total questions in database: {LifestyleQuestion.objects.count()}'
            )
        )




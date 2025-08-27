# management/commands/load_sample_questions.py
# Create directory: your_app/management/commands/

from django.core.management.base import BaseCommand
from myapp.models import Question

class Command(BaseCommand):
    help = 'Load sample pregnancy food questions into database'

    def handle(self, *args, **options):
        sample_questions = [
            {
                'question_text': 'Is it safe to eat sushi during pregnancy?',
                'option_a': 'Yes, all sushi is safe during pregnancy',
                'option_b': 'No, all sushi should be avoided',
                'option_c': 'Only cooked sushi and vegetarian rolls are recommended',
                'option_d': 'Only if from expensive restaurants',
                'correct_answer': 'Only cooked sushi and vegetarian rolls are recommended',
                'explanation': 'Raw fish can contain harmful bacteria and parasites. Cooked sushi and vegetarian options are safer choices.'
            },
            {
                'question_text': 'Can pregnant women drink coffee?',
                'option_a': 'No coffee at all during pregnancy',
                'option_b': 'Up to 200mg of caffeine per day is generally considered safe',
                'option_c': 'Unlimited coffee is fine',
                'option_d': 'Only decaffeinated coffee',
                'correct_answer': 'Up to 200mg of caffeine per day is generally considered safe',
                'explanation': 'Most health organizations recommend limiting caffeine to 200mg per day during pregnancy (about 1-2 cups of coffee).'
            },
            {
                'question_text': 'Are soft cheeses safe during pregnancy?',
                'option_a': 'All soft cheeses are safe',
                'option_b': 'Only unpasteurized soft cheeses should be avoided',
                'option_c': 'All soft cheeses should be avoided',
                'option_d': 'Only blue cheeses are dangerous',
                'correct_answer': 'Only unpasteurized soft cheeses should be avoided',
                'explanation': 'Pasteurized soft cheeses are generally safe. Unpasteurized versions may contain Listeria bacteria.'
            },
            {
                'question_text': 'Is it safe to eat deli meats during pregnancy?',
                'option_a': 'Yes, all deli meats are safe',
                'option_b': 'No, all deli meats should be avoided',
                'option_c': 'Only if heated until steaming hot',
                'option_d': 'Only organic deli meats are safe',
                'correct_answer': 'Only if heated until steaming hot',
                'explanation': 'Deli meats can harbor Listeria. Heating until steaming hot kills potential bacteria.'
            },
            {
                'question_text': 'Can pregnant women eat eggs?',
                'option_a': 'No eggs during pregnancy',
                'option_b': 'Only egg whites are safe',
                'option_c': 'Yes, but they should be fully cooked',
                'option_d': 'Only organic eggs are safe',
                'correct_answer': 'Yes, but they should be fully cooked',
                'explanation': 'Fully cooked eggs are safe and nutritious. Raw or undercooked eggs may contain Salmonella.'
            },
            {
                'question_text': 'Is alcohol consumption safe in any amount during pregnancy?',
                'option_a': 'Small amounts are fine',
                'option_b': 'Only wine is safe',
                'option_c': 'No amount of alcohol is considered safe',
                'option_d': 'Only during the second trimester',
                'correct_answer': 'No amount of alcohol is considered safe',
                'explanation': 'No level of alcohol consumption is considered safe during pregnancy as it can cause fetal alcohol spectrum disorders.'
            },
            {
                'question_text': 'Can pregnant women eat fish?',
                'option_a': 'No fish during pregnancy',
                'option_b': 'Yes, but limit high-mercury fish and eat 2-3 servings of low-mercury fish per week',
                'option_c': 'Only canned fish is safe',
                'option_d': 'Only freshwater fish is safe',
                'correct_answer': 'Yes, but limit high-mercury fish and eat 2-3 servings of low-mercury fish per week',
                'explanation': 'Fish is nutritious but some contain high mercury levels. Salmon, sardines, and anchovies are good low-mercury choices.'
            },
            {
                'question_text': 'Are artificial sweeteners safe during pregnancy?',
                'option_a': 'All artificial sweeteners are dangerous',
                'option_b': 'Most FDA-approved artificial sweeteners are safe in moderation',
                'option_c': 'Only stevia is safe',
                'option_d': 'Only during the third trimester',
                'correct_answer': 'Most FDA-approved artificial sweeteners are safe in moderation',
                'explanation': 'FDA-approved sweeteners like aspartame, sucralose, and stevia are generally considered safe in normal amounts.'
            },
            {
                'question_text': 'Should pregnant women avoid all herbal teas?',
                'option_a': 'Yes, all herbal teas are dangerous',
                'option_b': 'No, all herbal teas are safe',
                'option_c': 'Some are safe, but many should be avoided - consult healthcare provider',
                'option_d': 'Only green tea is safe',
                'correct_answer': 'Some are safe, but many should be avoided - consult healthcare provider',
                'explanation': 'Some herbal teas are safe (like ginger tea), but others may cause complications. Always check with your healthcare provider.'
            },
            {
                'question_text': 'Is it safe to eat peanuts during pregnancy?',
                'option_a': 'No, peanuts cause allergies in babies',
                'option_b': 'Yes, unless the mother has a peanut allergy',
                'option_c': 'Only organic peanuts are safe',
                'option_d': 'Only in the first trimester',
                'correct_answer': 'Yes, unless the mother has a peanut allergy',
                'explanation': 'Eating peanuts during pregnancy does not increase the risk of peanut allergies in children, unless the mother is allergic.'
            },
            {
                'question_text': 'Can pregnant women eat honey?',
                'option_a': 'No, honey contains botulism spores',
                'option_b': 'Yes, honey is safe for pregnant women',
                'option_c': 'Only raw honey is safe',
                'option_d': 'Only manuka honey is safe',
                'correct_answer': 'Yes, honey is safe for pregnant women',
                'explanation': 'Honey is safe for pregnant women. The concern about botulism spores applies only to infants under 12 months.'
            },
            {
                'question_text': 'Is it safe to eat sprouts during pregnancy?',
                'option_a': 'Yes, all sprouts are safe',
                'option_b': 'No, raw sprouts should be avoided due to bacteria risk',
                'option_c': 'Only homegrown sprouts are safe',
                'option_d': 'Only cooked sprouts are safe',
                'correct_answer': 'No, raw sprouts should be avoided due to bacteria risk',
                'explanation': 'Raw sprouts can harbor harmful bacteria like E. coli and Salmonella. Cooked sprouts are safer.'
            },
            {
                'question_text': 'Can pregnant women eat ice cream?',
                'option_a': 'No ice cream during pregnancy',
                'option_b': 'Only homemade ice cream is safe',
                'option_c': 'Yes, commercially made ice cream with pasteurized ingredients is safe',
                'option_d': 'Only soft-serve is safe',
                'correct_answer': 'Yes, commercially made ice cream with pasteurized ingredients is safe',
                'explanation': 'Commercial ice cream made with pasteurized dairy is safe. Avoid soft-serve from machines that may not be properly cleaned.'
            },
            {
                'question_text': 'Should pregnant women avoid all processed foods?',
                'option_a': 'Yes, all processed foods are harmful',
                'option_b': 'No, moderation is key - focus on nutritious whole foods when possible',
                'option_c': 'Only canned foods should be avoided',
                'option_d': 'Only frozen foods should be avoided',
                'correct_answer': 'No, moderation is key - focus on nutritious whole foods when possible',
                'explanation': 'While fresh, whole foods are ideal, some processed foods can be part of a healthy pregnancy diet. Read labels and choose wisely.'
            },
            {
                'question_text': 'Is it safe to eat unwashed fruits and vegetables during pregnancy?',
                'option_a': 'Yes, if they are organic',
                'option_b': 'No, all produce should be thoroughly washed',
                'option_c': 'Only fruits need washing',
                'option_d': 'Only vegetables need washing',
                'correct_answer': 'No, all produce should be thoroughly washed',
                'explanation': 'All fruits and vegetables should be thoroughly washed to remove potential bacteria, parasites, and pesticide residues.'
            },
            {
                'question_text': 'Can pregnant women eat liver?',
                'option_a': 'Yes, liver is very nutritious',
                'option_b': 'No, liver should be completely avoided',
                'option_c': 'Small amounts occasionally are okay, but regular consumption should be avoided',
                'option_d': 'Only chicken liver is safe',
                'correct_answer': 'Small amounts occasionally are okay, but regular consumption should be avoided',
                'explanation': 'Liver is high in vitamin A, and too much can be harmful to the developing baby. Occasional small amounts are generally safe.'
            },
            {
                'question_text': 'Is it safe to eat shellfish during pregnancy?',
                'option_a': 'No shellfish during pregnancy',
                'option_b': 'Yes, but only if thoroughly cooked',
                'option_c': 'Only canned shellfish is safe',
                'option_d': 'Only shrimp is safe',
                'correct_answer': 'Yes, but only if thoroughly cooked',
                'explanation': 'Thoroughly cooked shellfish is safe and nutritious. Raw or undercooked shellfish may contain harmful bacteria.'
            },
            {
                'question_text': 'Can pregnant women drink herbal supplements?',
                'option_a': 'Yes, all herbal supplements are natural and safe',
                'option_b': 'No, all herbal supplements should be avoided',
                'option_c': 'Only with healthcare provider approval',
                'option_d': 'Only prenatal herbal supplements',
                'correct_answer': 'Only with healthcare provider approval',
                'explanation': 'Many herbal supplements can interact with medications or affect pregnancy. Always consult your healthcare provider first.'
            },
            {
                'question_text': 'Is it safe to eat leftover food during pregnancy?',
                'option_a': 'No, never eat leftovers',
                'option_b': 'Yes, if properly stored and reheated to steaming hot',
                'option_c': 'Only if less than 24 hours old',
                'option_d': 'Only cold leftovers are safe',
                'correct_answer': 'Yes, if properly stored and reheated to steaming hot',
                'explanation': 'Properly refrigerated leftovers that are reheated to steaming hot are safe. Use within 3-4 days of cooking.'
            },
            {
                'question_text': 'Can pregnant women eat nuts?',
                'option_a': 'No nuts during pregnancy',
                'option_b': 'Yes, nuts are healthy unless the mother has allergies',
                'option_c': 'Only almonds are safe',
                'option_d': 'Only in the second trimester',
                'correct_answer': 'Yes, nuts are healthy unless the mother has allergies',
                'explanation': 'Nuts are nutritious and safe during pregnancy unless the mother has specific allergies. They provide healthy fats and protein.'
            },
            {
                'question_text': 'Is it safe to eat street food during pregnancy?',
                'option_a': 'Yes, if it looks fresh',
                'option_b': 'No, street food should generally be avoided',
                'option_c': 'Only vegetarian street food is safe',
                'option_d': 'Only if from familiar vendors',
                'correct_answer': 'No, street food should generally be avoided',
                'explanation': 'Street food may not be prepared under sanitary conditions and could contain harmful bacteria. It\'s safer to avoid during pregnancy.'
            },
            {
                'question_text': 'Can pregnant women eat chocolate?',
                'option_a': 'No chocolate during pregnancy',
                'option_b': 'Yes, in moderation chocolate is fine',
                'option_c': 'Only white chocolate is safe',
                'option_d': 'Only dark chocolate is safe',
                'correct_answer': 'Yes, in moderation chocolate is fine',
                'explanation': 'Chocolate in moderation is safe during pregnancy. It contains caffeine, so factor it into your daily caffeine limit.'
            },
            {
                'question_text': 'Should pregnant women avoid all canned foods?',
                'option_a': 'Yes, all canned foods contain harmful chemicals',
                'option_b': 'No, many canned foods are safe and nutritious',
                'option_c': 'Only canned fruits are safe',
                'option_d': 'Only canned vegetables are safe',
                'correct_answer': 'No, many canned foods are safe and nutritious',
                'explanation': 'Many canned foods are safe and can be part of a healthy diet. Choose low-sodium options and rinse when appropriate.'
            },
            {
                'question_text': 'Is it safe to eat pickled foods during pregnancy?',
                'option_a': 'No, pickled foods are too acidic',
                'option_b': 'Yes, pickled foods are safe in moderation',
                'option_c': 'Only homemade pickles are safe',
                'option_d': 'Only sweet pickles are safe',
                'correct_answer': 'Yes, pickled foods are safe in moderation',
                'explanation': 'Pickled foods are generally safe during pregnancy. They can be high in sodium, so consume in moderation.'
            },
            {
                'question_text': 'Can pregnant women eat spicy food?',
                'option_a': 'No, spicy food can harm the baby',
                'option_b': 'Yes, spicy food is safe if tolerated well',
                'option_c': 'Only mild spices are safe',
                'option_d': 'Only in the first trimester',
                'correct_answer': 'Yes, spicy food is safe if tolerated well',
                'explanation': 'Spicy foods are safe during pregnancy and may even help baby develop taste preferences. Avoid if they cause discomfort.'
            }
        ]

        created_count = 0
        for question_data in sample_questions:
            question, created = Question.objects.get_or_create(
                question_text=question_data['question_text'],
                defaults=question_data
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded {created_count} new questions. Total questions in database: {Question.objects.count()}'
            )
        )
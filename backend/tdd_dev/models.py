from django.db import models

class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Question(models.Model):
    QUESTION_TYPES = [
        ("multiple_choice", "Multiple Choice"),
        ("rating", "Rating"),
        ("text", "Open Text"),
        ("dropdown", "Dropdown"),
        ("checkbox", "Checkbox"),
    ]
    id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(Survey, related_name="questions", on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    condition_question = models.ForeignKey(
        'self', null=True, blank=True, related_name='conditional_questions', on_delete=models.CASCADE
    )
    condition_answer = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()  # enforce field validation
        super().save(*args, **kwargs)


class QuestionOption(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
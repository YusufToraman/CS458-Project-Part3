from ...models import Survey, Question, QuestionOption
from rest_framework.exceptions import ValidationError


class SurveyBuilder:
    def __init__(self, validated_data):
        self.title = validated_data["title"].strip()
        self.questions = validated_data["questions"]
        self.seen_question_texts = set()
        self.uuid_to_question_data = {}
        self.uuid_to_instance = {}

    def validate_business_rules(self):
        for q in self.questions:
            number = q["number"]
            text = q["question_text"].strip()
            q_type = q["question_type"]
            cond_q = q.get("condition_question")
            cond_ans = q.get("condition_answer", "").strip()
            options = q.get("options", [])

            if text in self.seen_question_texts:
                raise ValidationError(f"Duplicate question text: '{text}'.")
            self.seen_question_texts.add(text)

            if q_type in {"multiple_choice", "dropdown", "checkbox"}:
                if not options:
                    raise ValidationError(f"Options required for question '{text}'.")
                seen_opts = set()
                for opt in options:
                    opt_text = opt["text"].strip()
                    if not opt_text:
                        raise ValidationError(f"Empty option in question '{text}'.")
                    if opt_text in seen_opts:
                        raise ValidationError(f"Duplicate option text '{opt_text}' in question '{text}'.")
                    seen_opts.add(opt_text)

            if cond_q:
                if cond_q == number:
                    raise ValidationError(f"Question {number} cannot depend on itself.")
                if not any(q2["number"] == cond_q for q2 in self.questions):
                    raise ValidationError(f"Invalid condition_question reference: {cond_q}")
                if not cond_ans:
                    raise ValidationError(f"Missing condition_answer for question '{text}'.")

            self.uuid_to_question_data[number] = q

        self._check_circular_dependency()

    def _check_circular_dependency(self):
        for q in self.questions:
            num = q["number"]
            cond = q.get("condition_question")
            if cond:
                other = self.uuid_to_question_data.get(cond)
                if other and other.get("condition_question") == num:
                    raise ValidationError(f"Circular dependency between questions '{num}' and '{cond}'.")

    def build(self):
        survey = Survey.objects.create(title=self.title)

        for q in self.questions:
            question = Question.objects.create(
                survey=survey,
                question_text=q["question_text"].strip(),
                question_type=q["question_type"]
            )
            self.uuid_to_instance[q["number"]] = question

        for q in self.questions:
            question = self.uuid_to_instance[q["number"]]
            cond_uuid = q.get("condition_question")

            if cond_uuid:
                question.condition_question = self.uuid_to_instance.get(cond_uuid)
                question.condition_answer = q.get("condition_answer", "").strip()
                question.save()

            if question.question_type in {"multiple_choice", "dropdown", "checkbox"}:
                for opt in q.get("options", []):
                    text = opt["text"].strip()
                    if text:
                        QuestionOption.objects.create(question=question, text=text)

        return survey

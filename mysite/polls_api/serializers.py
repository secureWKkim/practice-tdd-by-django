from rest_framework import serializers
from polls.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date']
    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Question.objects.create(**validated_data)  # **kwargs

    def update(self, instance, validated_data):  # instance = 있던 것
        # (넣어줄 값, 그게 없을 경우 채워줄 값). 여기서 후자는 원래 있던 값이며, OrderedDict다.
        instance.question_text = validated_data.get('question_text', instance.question_text)
        instance.save()
        return instance
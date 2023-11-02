from rest_framework import serializers
from polls.models import Question
from django.contrib.auth.models import User


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'owner']
    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        return Question.objects.create(**validated_data)  # **kwargs

    def update(self, instance, validated_data):  # instance = 있던 것
        # (넣어줄 값, 그게 없을 경우 채워줄 값). 여기서 후자는 원래 있던 값이며, OrderedDict다.
        instance.question_text = validated_data.get('question_text', instance.question_text)
        instance.save()
        return instance
    

class UserSerializer(serializers.ModelSerializer):
    """
    PrimaryKeyRelatedField는 class인 User의 PrimaryKey를 통해서 여러 개의 question을 가지고 있다고 명시한 것
    fields에 추가하지 않고 따로 선언한 이유는
    User 테이블에 있는 것이 아니라 Question 테이블에 있는 user_id라는 필드가 있고,
    그걸 통해서 User는 Question을 불러올 수 있는 것이기 때문
    """
    questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
    
    class Meta:
        model = User
        fields = ['id', 'username', 'questions']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "두 패스워드가 일치하지 않습니다."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        
        return user
    
    class Meta:
        model = User
        fields = ['username', 'password','password2']
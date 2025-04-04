import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct
    
def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_set_correct_choices_marks_them_correctly():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    question.set_correct_choices([c1.id, c2.id])
    assert c1.is_correct is True
    assert c2.is_correct is True

def test_select_choices_returns_only_correct_ids():
    question = Question(title='q1', max_selections=3)
    c1 = question.add_choice('a')
    c2 = question.add_choice('b', is_correct=True)
    c3 = question.add_choice('c', is_correct=True)
    selected = question.select_choices([c1.id, c2.id, c3.id])
    assert selected == [c2.id, c3.id]

def test_generate_ids_are_incremented():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    c3 = question.add_choice('c')
    assert [c1.id, c2.id, c3.id] == [1, 2, 3]

def test_create_multiple_choices_and_check_values():
    question = Question(title='q1')
    c1 = question.add_choice('a', False)
    c2 = question.add_choice('b', True)

    assert len(question.choices) == 2
    assert c1.text == 'a' and not c1.is_correct
    assert c2.text == 'b' and c2.is_correct

def test_choice_ids_reflect_added_choices():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    ids = [choice.id for choice in question.choices]
    assert ids == [c1.id, c2.id]

def test_remove_choice_by_id_removes_correctly():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    question.remove_choice_by_id(c2.id)
    remaining_ids = [choice.id for choice in question.choices]
    assert remaining_ids == [c1.id]

def test_remove_choice_and_add_another_correctly():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    question.remove_choice_by_id(c1.id)
    c3 = question.add_choice('c')
    remaining_ids = [choice.id for choice in question.choices]
    assert c3.id == c2.id + 1
    assert remaining_ids == [c2.id, c3.id]

def test_remove_all_choices_clears_list():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_select_more_choices_than_max_raises_exception():
    question = Question(title='q1', max_selections=1)
    question.add_choice('a', True)
    with pytest.raises(Exception):
        question.select_choices([999, 54])
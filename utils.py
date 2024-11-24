import json

def load_course_test(course_number):
    """
    Загружает тест для указанного курса из JSON файла
    Args:
        course_number: номер курса
    Returns:
        dict: данные теста или None, если тест не найден
    """
    try:
        with open('course_tests.json', 'r', encoding='utf-8') as f:
            tests = json.load(f)
            return tests.get(str(course_number))
    except FileNotFoundError:
        return None

def generate_test_html(course_number):
    """
    Генерирует HTML код теста для указанного курса
    Args:
        course_number: номер курса
    Returns:
        str: HTML код теста или None, если тест не найден
    """
    test_data = load_course_test(course_number)
    if not test_data:
        return None
    
    html = f'<h4>{test_data["title"]}</h4>\n'
    html += '<form id="quiz" action="/course{}" method="POST">\n'.format(course_number)
    html += '    <div>\n'
    
    for question in test_data['questions']:
        html += f'''
        <div class="quiztion">
            <p>{question["id"]}. {question["text"]}</p>
            <div class="btn-group col-md-12">
        '''
        
        for answer in question['answers']:
            html += f'''
                <input type="radio" class="btn-check" 
                       name="q{question['id']}" 
                       id="q{question['id']}_{answer['id']}" 
                       autocomplete="off" 
                       value="{answer['id']}" />
                <label class="btn" for="q{question['id']}_{answer['id']}" 
                       data-mdb-ripple-init>{answer['text']}</label>
            '''
        
        html += '''
            </div>
        </div>
        '''
    
    html += '''
        <input type="submit" value="Сдать тест" 
               id="checkAnswers" class="btn btn-primary col-md-12">
    </div>
</form>

<script>
    // Функция для отправки результатов в БД
    async function postTestResults(answers, timestamp, student_id) {
        try {
            const response = await fetch('/submit_test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    course_id: window.COURSE_NUMBER,
                    answers: answers,
                    timestamp: timestamp,
                    user_id: student_id
                })
            });
            return await response.json();
        } catch (error) {
            console.error('Ошибка при сохранении результатов:', error);
        }
    }

    document.getElementById('quiz').addEventListener('submit', function (event) {
        event.preventDefault();
        const answers = {};
        const questions = this.querySelectorAll('.quiztion');
        
        // Собираем ответы
        let allAnswered = true;
        questions.forEach(function(question, index) {
            const selected = question.querySelector('input[type="radio"]:checked');
            if (!selected) {
                allAnswered = false;
            } else {
                answers[index + 1] = selected.value;
            }
        });
        
        if (!allAnswered) {
            alert('Вы не ответили на все вопросы');
            return;
        }
        
        // Отправляем ответы на сервер
        fetch('/course' + window.COURSE_NUMBER, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(answers)
        })
        .then(response => response.json())
        .then(async data => {
            const timestamp = Date.now();
            // Сохраняем результаты в базу с передачей всех необходимых аргументов
            await postTestResults(answers, timestamp, window.USER_ID);
            // Показываем сообщение об успешной отправке
            alert('Тест успешно сдан');
            // Отключаем форму
            document.getElementById('quiz').style.pointerEvents = 'none';
            document.getElementById('quiz').style.opacity = '0.7';
        });
    });
</script>
    '''
    
    return html 
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Класс для заметки
class Note:
    def __init__(self, topic, title, content, tag=None):
        self.topic = topic
        self.title = title
        self.content = content
        self.tag = tag  # Добавим тег для заметки

    def update_content(self, new_content):
        self.content = new_content

    def update_title(self, new_title):
        self.title = new_title

    def update_topic(self, new_topic):
        self.topic = new_topic

    def display(self):
        return f"Topic: {self.topic}\nTitle: {self.title}\nContent: {self.content}"

# Класс для тега
class Tag:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

# Класс для управления заметками
class NoteManager:
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def get_notes_by_topic(self, topic):
        return [note for note in self.notes if note.topic == topic]

    def get_all_topics(self):
        return list({note.topic for note in self.notes})

    def get_note_by_title(self, title):
        for note in self.notes:
            if note.title == title:
                return note
        return None

    def delete_note_by_title(self, title):
        self.notes = [note for note in self.notes if note.title != title]

note_manager = NoteManager()

@app.route('/dlyachegozametki', methods=['GET', 'POST'])
def dlyachegozametki():
    return render_template('dlyachegozametki.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/')
def index():
    topics = note_manager.get_all_topics()  # Получаем уникальные темы
    return render_template("index.html.j2", topics=topics)


@app.route('/topic/<string:topic>')
def topic(topic):
    topic_notes = note_manager.get_notes_by_topic(topic) # Фильтруем заметки по теме
    if not topic_notes:
        return f"No notes found for topic: {topic}", 404  # Если заметки для темы не найдены, возвращаем ошибку 404
    return render_template("topic.html", notes=topic_notes, topic=topic)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        topic = request.form['topic']
        title = request.form['title']
        content = request.form['content']
        tag_name = request.form.get('tag', '')  # Получаем тег, если он был введен

        # Создаем объект Tag, если тег не пустой
        tag = Tag(tag_name) if tag_name else None

        # Создаем объект Note с тегом и добавляем его в NoteManager
        new_note = Note(topic, title, content, tag)
        note_manager.add_note(new_note)
        
        return redirect(url_for('index'))
    return render_template("create.html")

# Удаление заметки
@app.route('/delete/<string:title>', methods=['POST'])
def delete(title):
    note_manager.delete_note_by_title(title)
    return redirect(url_for('index'))

# Редактирование заметки
@app.route('/edit/<string:title>', methods=['GET', 'POST'])
def edit(title):
    note = note_manager.get_note_by_title(title)
    if not note:
        return "Note not found", 404

    if request.method == 'POST':
        note.update_topic(request.form['topic'])
        note.update_title(request.form['title'])
        note.update_content(request.form['content'])
        return redirect(url_for('index'))
    
    return render_template("edit.html", note=note)

if __name__ == '__main__':
    app.run(debug=True)

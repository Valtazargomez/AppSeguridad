from flask import Flask, request, redirect, url_for, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required as flask_login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuración de la base de datos (SQLite para este ejemplo)
app.config.from_pyfile('config.py')

# Inicialización de SQLAlchemy
db = SQLAlchemy(app)

# Inicialización de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Define la ruta para el inicio de sesión

# Definición del modelo de usuario (implementando UserMixin)
class User(db.Model, UserMixin):
    __tablename__ = 'TBLSEGURIDAD'

    id = db.Column(db.Integer, primary_key=True)  # Flask-Login requiere un atributo 'id'
    StrUsuario = db.Column(db.String(80), unique=True, nullable=False)
    StrClaveHash = db.Column(db.String(128), nullable=False)  # Cambiamos StrClave a StrClaveHash
    StrRol = db.Column(db.String(20), default='usuario') # Agregamos un campo para el rol

    def set_password(self, password):
        """Genera el hash de la contraseña."""
        self.StrClaveHash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña hasheada."""
        return check_password_hash(self.StrClaveHash, password)

    def __repr__(self):
        return f'<User {self.StrUsuario} ({self.StrRol})>'

# Callback para cargar el usuario desde la sesión
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Creación de la base de datos y usuarios de prueba con roles
with app.app_context():
    db.create_all()
    if not User.query.filter_by(StrUsuario='admin').first():
        admin_user = User(StrUsuario='admin', StrRol='admin')
        admin_user.set_password('adminpassword')
        db.session.add(admin_user)
    if not User.query.filter_by(StrUsuario='testuser').first():
        test_user = User(StrUsuario='testuser', StrRol='usuario')
        test_user.set_password('testpassword')
        db.session.add(test_user)
    db.session.commit()

# Rutas de la aplicación
@app.route('/')
@flask_login_required
def index():
    return render_template('index.html', username=current_user.StrUsuario)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(StrUsuario=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            error = 'Credenciales incorrectas. Por favor, inténtalo de nuevo.'
    return render_template('login.html', error=error)

@app.route('/logout')
@flask_login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.after_request
def set_secure_headers(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')
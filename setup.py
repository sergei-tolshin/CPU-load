from setuptools import find_packages, setup

if __name__ == '__main__':
    setup(
        name='cpuload',
        version='1.0',
        packages=find_packages(),
        description='CPU Load app',
        author='Sergei Tolshin',
        author_email='tolshin.sergei@yandex.ru',
        include_package_data=True,
        install_requires=[
            'flasgger==0.9.5',
            'Flask==2.2.2',
            'Flask-Babel==2.0.0',
            'flask-marshmallow==0.14.0',
            'Flask-Migrate==4.0.0',
            'Flask-SQLAlchemy==3.0.2',
            'marshmallow-sqlalchemy==0.28.1',
            'SQLAlchemy==1.4.45',
            'SQLAlchemy-Utils==0.39.0',
            'python-dotenv==0.21.0',
        ],
        entry_points={
            'console_scripts': [
                'cpuload = src.manage:run_server',
            ]
        },
    )

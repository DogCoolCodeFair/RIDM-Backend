<h2 align="center"> RIDM </h3>

<h6 align="center">본 프로젝트는 과학기술정보통신부 주최의 한국코드페어에 출품하여 수상한 작품입니다.<br>
This project was submitted to the Korea Code Fair hosted by the Ministry of Science and ICT and won the award.

<h6 align="center">
Backend Developed By <a href="https://github.com/331leo">@331leo</a> (Donghyun Kim)<br>
Frontend Developed By <a href="https://github.com/fxrcha">@fxrcha</a> (Hyunwoo Cho)<br>
Project Idea Provided By <a href="https://github.com/winstar0070">@winstar0070</a> (Yunseok Hong)
</h5>

<h3 align="center"> Contents </h3>
<div align="center">
<a href="#project-presentation">1. Project Presentation</a>
<a href="#project-poster">2. Project Poster</a>
<a href="#backend-installation">3. Backend Installation</a>
</div>

---

## Project Presentation

![page1](./images/Slide%2016_9%20-%201.png)
![page2](./images/Slide%2016_9%20-%202.png)
![page3](./images/Slide%2016_9%20-%203.png)
![page4](./images/Slide%2016_9%20-%204.png)
![page5](./images/Slide%2016_9%20-%205.png)
![page6](./images/Slide%2016_9%20-%206.png)
![page7](./images/Slide%2016_9%20-%207.png)
![page8](./images/Slide%2016_9%20-%208.png)
![page9](./images/Slide%2016_9%20-%209.png)

## Project Poster

![poster](./images/Frame%20135.png)

## Backend Installation

**_This Project uses [Poetry Package Manager](https://github.com/python-poetry/poetry)_**

```bash
poetry install
```

### Run Server via uvicorn (Development)

```bash
poetry run uvicorn app:app --reload
```

### Run Server via gunicorn (Production)

```bash
(Configure Appliction Settings on gunicorn.conf.py)
poetry run gunicorn app:app
```

## Docs

[Swagger](https://api.dogcoolcodefair.com/docs/swagger), [Redoc](https://api.dogcoolcodefair.com/docs/redoc)

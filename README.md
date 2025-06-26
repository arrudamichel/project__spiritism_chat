# Spiritism chat

Our specialized Spiritism chat system offers a unique and educational platform for those seeking a deeper understanding of this spiritual philosophy. Powered by a diverse and carefully curated collection of sources—including books, videos, audios, and web pages—the system is equipped to answer questions and clarify doubts about the principles, practices, and teachings of Spiritism.

**Key Features:**

- **Reliable Sources**: Responses are grounded in essential Spiritist works, including the books of Allan Kardec, audiovisual materials, and trustworthy Spiritist websites, ensuring comprehensive and well-supported information.

- **Wide Range of Topics**: The system covers a broad spectrum of themes, from the immortality of the soul and reincarnation to moral laws and mediumship.

- **Intuitive Interface**: The platform is user-friendly, allowing users to ask questions directly in the chat and receive precise and well-founded answers.

- **Continuous Improvement**: The system is constantly updated, incorporating new content from books, videos, lectures, podcasts, and web articles to ensure the information remains relevant and up-to-date.

- **Ethical Guidance**: In addition to answering questions, the system aims to promote the values of fraternity, charity, and respect, aligned with Spiritist principles.

- **Accessibility**: Available 24/7, the chat provides immediate access to information and clarifications, facilitating the study and practice of Spiritism.

**Objective:**

Our goal is to provide a learning and consultation tool that facilitates access to Spiritist knowledge, contributing to the spiritual and moral development of users. Through the combined wisdom of Spiritist books, audiovisual content, and digital resources, we aim to offer clear and profound answers, helping to build a solid and comprehensive understanding of this spiritual philosophy.

Explore, ask, and discover more about Spiritism with our dedicated chat system!

## Architeture

![architeture image](https://github.com/arrudamichel/project__spiritism_chat/blob/main/image/LLM%20Spiritism%20Chat.png)

## Instalation

The project has 3 differents environments: experimentation, API and Webpage. Follow the steps to install the environments.

## Experimentation

To install and activate environment:
```
conda env create -f experimentation/environment.yml
conda activate spiritism-chat
```

To run the notebooks:
```
jupyter-lab
```

To access the notebook:

```
http://localhost:8888/lab
```

## API

To install and activate environment:
```
conda env create -f api/environment.yml
conda activate spiritism-chat-api
```


To run the API:
```
uvicorn main:app --reload --port 8000
```

To access the documentation from API:

```
http://localhost:8080/docs
```

## Webpage

To install and activate environment:
```
conda env create -f webpage/environment.yml
conda activate spiritism-chat-webpage
```

To run the page:

```
cd webpage/
streamlit run app.py --server.port 8502
```

To access de page:
```
http://localhost:8502/
```

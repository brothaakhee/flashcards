=============================
Flashcards Learning Platform
=============================

This is a flashcard-style learning platform developed using Django, Django Rest Framework, and Vue.js.

Features
========

1. User Registration and Authentication
----------------------------------------

Users can register for a new account, log in, and log out. User authentication is managed with Django's built-in user management.

2. Word Management
-------------------

After logging in, users can add new words they want to learn, along with a definition. These words are then used to generate flashcards for review. Users can view all the words they have added in a tabular format, with the ability to delete any word.

3. Flashcard Review
-------------------

Users can review the words they've added in a flashcard-style interface. A word is presented without its definition, and users can choose to reveal the definition. 

4. Spaced Repetition Learning
------------------------------

The app employs a spaced repetition algorithm to enhance the user's learning. Words are sorted into different bins based on how well the user knows them. If the user recalls a word correctly, it moves to the next bin, indicating a longer time until it should be reviewed again. If the user fails to recall a word, it moves back to an earlier bin, ensuring it will be reviewed sooner.

If the user answers incorrectly 10 times, the card will not be shown again.
Similarly, if the user answers a Card correctly enough times, it will also not
be shown again.

Potential Improvements
========

- Right now, everything is under the `cards` app, even registration and login
  views. Ideally these should be contained within a `users` app, or top level
  urls.
- The User Words view is using bootstrap styled table. Would be nice to be able
  to search, filter, and order based on columns.
- There is some duplication in the templates, could use some
  cleanup/consolidation.
- Have a bulk word/definition creation tool for the user, so they don't have to
  create each word individually
- Spruce up UI/UX

Getting Started
===============

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
-------------

You will need the following tools:

- Python 3.8+
- Django 3.2+
- Django Rest Framework
- Vue.js 2.0+

Installation
------------

Clone the repository:

.. code:: bash

    git clone https://github.com/brothaakhee/flashcards.git
    cd flashcards

Install Python dependencies:

.. code:: bash

    pip install -r requirements.txt

Run migrations:

.. code:: bash

    python manage.py migrate

Run the development server:

.. code:: bash

    python manage.py runserver

The application should now be accessible at `http://localhost:8000/`

Running Tests
-------------

To run the tests, execute:

.. code:: bash

    pytest

Acknowledgments
===============

- Thanks to OpenAI for the GPT-4 model.

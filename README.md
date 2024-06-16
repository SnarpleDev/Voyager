# Voyager
A magic Scratch indexer.

## How to start
Clone the repo.

Then, install SurrealDB. After running ``./surreal.sh``, you'll get something like ``SurrealDB successfully installed in: <path>``. Copy that path and move it to ``/usr/local/bin``.

Create a file called ``.env`` following ``.env.example`` and run ``source .env``.

Then, on a terminal, run ``surreal start --allow-all --auth --user $USERNAME --pass $PASSWORD file://voyagerdb``. This will start the Surreal server.

On another terminal, run ``surreal import --namespace Voyager --database Voyager voyager.surql --endpoint http://localhost:8000 --user $USERNAME --pass $PASSWORD``. Make sure port 8000 is open. This will import the Voyager database schema.

Finally, run ``pip install -r requirements.txt -q``, and you're ready to go!
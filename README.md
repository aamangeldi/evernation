# EverNation
0. Clone the repo:
    ```
    git clone git@github.com:aamangeldi/evernation.git
    ```
1. Obtain `credentials.json` and put in the top-most directory.
2. Create a `secret.yml` and fill in missing pieces:
    ```
    cp config/secret.yml.example config/secret.yml
    ```
3. Run the following to authenticate your Google account and generate token:
    ```
    pip install -r requirements.txt
    python sheets.py
    ```
4. Run:
    ```
    docker-compose up
    ```
5. Navigate to `localhost:5000`

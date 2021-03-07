# toggl-to-sqlite

Create a SQLite database containing data from your [Toggl](https://toggl.com/) account.

## How to install

    $ pip install toggl-to-sqlite

## Usage

You will need to first obtain a valid OAuth token for your toggl account. You can do this by running the `auth` command and following the prompts:

    $ toggl-to-sqlite auth
    You will need to get your API Token from this page

    https://track.toggl.com/profile...

    Once you have your API Token enter it at the command line. 
    
    Authentication tokens written to auth.json

Now you can fetch all of your items from toggl like this:

    $ toggl-to-sqlite fetch toggl.db

The first time you run this command it will fetch all of your items, and display a progress bar while it does it.

## Using with Datasette

The SQLite database produced by this tool is designed to be browsed using [Datasette](https://datasette.readthedocs.io/). Use the [datasette-render-timestamps](https://github.com/simonw/datasette-render-timestamps) plugin to improve the display of the timestamp values.
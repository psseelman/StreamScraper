import os
import pafy
import pandas as pd


links = [
    "https://www.youtube.com/watch?v=VMCZZfKYC_Q"
]


def check_youtube(url):
    video: pafy.pafy
    try:
        video = pafy.new(url)
    except (IOError, OSError):
        return
    author = video.author.replace("\'", "")
    title = video.title.replace("\'", "")
    length = video.length
    view_count = video.viewcount
    source = "YouTube"
    id = video.videoid.replace("\'", "").replace("\"", "")
    is_live: bool
    if video.duration == "00:00:00":
        is_live = True
    else:
        is_live = False

    add_stream(id, author, title, is_live, length, view_count, source, url)


def did_update_csv():
    print()


def get_existing_row_index(dataframe):
    df = pd.read_csv("streams.csv", delimiter=",")

    row_values: list = dataframe.to_numpy()[0]

    id = row_values[0]
    author = row_values[1]

    id_frame = df.loc[df['id'] == id]
    author_frame = df.loc[df['author'] == author]

    if not id_frame.empty:
        return int(id_frame.index[0])
    elif not author_frame.empty:
        return int(author_frame.index[0])

    return None


def make_dataframe(id, author, title, is_live, length, view_count, source, url) -> pd.DataFrame:
    dataframe = pd.DataFrame({'id': [id], 'author': [author], 'title': [title], 'is_live': [is_live], 'length': [length], 'view_count': [view_count], 'source': [source], 'url': [url]})
    return dataframe


def update_row(index, dataframe):
    df = pd.read_csv("streams.csv", delimiter=",")
    df.update(dataframe)
    df.to_csv("streams.csv", index=False)
    did_update_csv()


def add_row(dataframe):
    df = pd.read_csv("streams.csv", delimiter=",")
    new_df = pd.concat([df, dataframe])
    new_df.to_csv("streams.csv", index=False)
    did_update_csv()


def add_stream(id, author, title, is_live, length, view_count, source):
    new_df = make_dataframe(id, author, title, is_live, length, view_count, source)
    row_index = get_existing_row_index(new_df)

    if row_index is None:
        add_row(new_df)
    else:
        update_row(row_index, new_df)


def main():
    pafy.set_api_key(os.environ['YOUTUBE_API_KEY'])
    for link in links:
        check_youtube(link)


if __name__ == "__main__":
    main()

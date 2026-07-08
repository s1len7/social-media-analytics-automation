from social_media_analytics.utils.config import load_config
from social_media_analytics.utils.logger import setup_logger
from social_media_analytics.collectors.instagram import collect_instagram_posts
from social_media_analytics.storage.csv_writer import save_csv


def main():

    config = load_config()

    logger = setup_logger(
        config["logging"]["level"]
    )

    logger.info("Social media analytics started")

    instagram_posts = []

    for account in config["instagram"]["accounts"]:

        logger.info(
            f"Collect Instagram account: {account}"
        )

        posts = collect_instagram_posts(
            account
        )

        instagram_posts.extend(posts)


    save_csv(
        instagram_posts,
        "data/raw/instagram_posts.csv"
    )

    logger.info("Completed")


if __name__ == "__main__":
    main()
from setuptools import setup, find_packages

setup(
    name="TgUserScanner",
    version="0.1.0",
    author="Vladimir Ivashkin",
    author_email="illusionww@gmail.com",
    description="A Python package to extract usernames from Telegram chats, channels, and direct messages.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vlivashkin/TgUserScanner",
    packages=find_packages(),
    install_requires=["telethon", "tqdm", "pandas"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

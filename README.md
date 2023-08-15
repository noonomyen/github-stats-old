## GitHub Stats
- drawing tool (svg card) : [inkscape](https://inkscape.org/)
- language scan in repository : [linguist](https://github.com/github/linguist)

### How it works ?
Check for updates If any changes are made, the SVG is generated and placed in the repo for the README and pushed to the repository.

#### Language counting
Use git blame to get your edited line and count the number of characters in the line.

### Setup
```
git clone https://github.com/noonomyen/github-stats
git submodule update --init
```

#### Install github-linguist
```
sudo apt-get install build-essential cmake pkg-config libicu-dev zlib1g-dev libcurl4-openssl-dev libssl-dev ruby-dev
gem install github-linguist
```

#### config.json
```
{
    "delay": 3600,
    "user": "<target-name>",
    "stats": "github-stats/stats.json",
    "svg": {
        "light": "github-stats/light.svg",
        "dark": "github-stats/dark.svg"
    },
    "auth": {
        "token": "<github-personal-access-token>",
        "name": "<user.name>",
        "email": "<user.email>"
    }
}
```

#### run
```
python github-stats.py --config config.json
```

### Example use with README.md

```
<picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-stats.noonomyen.com/noonomyen/dark.svg">
    <img src="https://github-stats.noonomyen.com/noonomyen/light.svg">
</picture>
```

<picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-stats.noonomyen.com/noonomyen/dark.svg">
    <img src="https://github-stats.noonomyen.com/noonomyen/light.svg">
</picture>

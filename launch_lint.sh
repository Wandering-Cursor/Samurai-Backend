docker build --tag "samurai-lint" --file lint.dockerfile .

docker run --rm -v "$(pwd):/app" samurai-lint
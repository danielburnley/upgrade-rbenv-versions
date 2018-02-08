# Ruby-upgrade-script

A script for mass updating repositories which use rbenv with `.ruby-version` files

## What this script will do

- Change the `.ruby-version` file to the version specified
- Run `bundle update`
- Commit the changes to both the `.ruby-version` and `Gemfile.lock`
- Run the tests and log whether or not they passed or failed

## Requirements

- rbenv
- The desired ruby version
- Python
- Bundler
- To run the tests:
  - Your tests must run by calling `bundle exec rake`

## How to run

1. Put the paths to your repos into a file called `repos.txt`
2. Run `python run.py <ruby version>`, e.g. `python run.py 2.5.0`
3. Watch the upgrade happen
4. Check `ruby-upgrade.log` to see the results of the test runs

### TODO

- Custom test commands
- Ability to hide stdout/stderr


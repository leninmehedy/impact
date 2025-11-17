# Impact - A GitHub PR List Generator

A Python script to fetch and list your Pull Requests from GitHub repositories within a specified date range.

## Prerequisites

- Python 3.6 or higher
- A GitHub Personal Access Token

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd impact
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory with the following settings:

```env
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_USERNAME=your_github_username
REPOS=owner/repo1,owner/repo2,owner/repo3
```

**Environment Variables Explanation:**

- `GITHUB_TOKEN`: Your GitHub Personal Access Token (required)
  - Create one at: https://github.com/settings/tokens
  - Required scopes: `repo` (for private repositories) or `public_repo` (for public repositories only)
  
- `GITHUB_USERNAME`: Your GitHub username (required)
  - This is used to filter PRs created by you
  
- `REPOS`: Comma-separated list of repositories to scan (optional)
  - Format: `owner/repository-name`
  - Example: `leninmehedy/impact,leninmehedy/another-repo`
  - If not provided, the script will scan all repositories you have access to (this may be slow)

## Usage

Run the script with a start date and end date:

```bash
python fetch.py <start_date> <end_date>
```

### Example

Fetch PRs created between November 1, 2025 and November 15, 2025:

```bash
python fetch.py 2025-11-01 2025-11-15
```

### Date Format

- Dates should be in ISO format: `YYYY-MM-DD`
- The script will include PRs created on both the start and end dates (inclusive)

## Output

The script will display:
- Repository name
- PR number and title
- PR URL

Example output:
```
=== Fetching PRs for owner/repository ===
- PR-123: Add new feature (owner/repository)
  https://github.com/owner/repository/pull/123
- PR-124: Fix bug (owner/repository)
  https://github.com/owner/repository/pull/124

=== Fetching PRs for another/repo ===
No PRs found in this date range or no access.
```

## Troubleshooting

### Authentication Errors

If you encounter authentication errors:
- Verify your `GITHUB_TOKEN` is valid and has not expired
- Ensure the token has the appropriate scopes (`repo` or `public_repo`)
- Check that your token is correctly set in the `.env` file

### Repository Access Errors

If you see "Error fetching" messages:
- Verify the repository names are in the correct format (`owner/repo`)
- Ensure you have access to the specified repositories
- Check if the repositories exist and are not deleted

### No PRs Found

If no PRs are displayed:
- Verify your `GITHUB_USERNAME` matches your GitHub username exactly
- Check that you created PRs within the specified date range
- Ensure the repositories contain PRs created by you

## Deactivating the Virtual Environment

When you're done, you can deactivate the virtual environment:

```bash
deactivate
```

## License

This project is open source and available under the MIT License.

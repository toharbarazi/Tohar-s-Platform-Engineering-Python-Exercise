
# HI! Welcome to Tohar's CLI
In this system you can remotely manage EC2, S3 and Route53 services in your AWS environment.
To install the system follow these steps:



## 1. Prerequisites

Before you begin, ensure you have the following:

- **AWS Account**: An active AWS account with appropriate permissions.
- **Python Installed**: Version 3.6 or higher.
- **Git Installed**: To clone the repository.

---

## 2. Install Required Software

### 2.1. Install Python

- **Download and Install**: Obtain the latest version of Python from the [official website](https://www.python.org/downloads/).
  - During installation, ensure you select the option to **"Add Python to PATH"**.

- **Verify Installation**:
  ```bash
  python --version
  ```

### 2.2. Install Git

- **Download and Install**: Get Git from the [official Git website](https://git-scm.com/downloads).

- **Verify Installation**:
  ```bash
  git --version
  ```

### 2.3. Install AWS CLI

- **Download and Install**: Follow the [AWS CLI installation guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).

- **Verify Installation**:
  ```bash
  aws --version
  ```

- **Configure AWS CLI**:
  ```bash
  aws configure
  ```
  Provide your AWS Access Key ID, Secret Access Key, default region, and output format when prompted.

### 2.4. Install Pulumi

- **Download and Install**: Instructions are available on the [Pulumi installation page](https://www.pulumi.com/docs/get-started/install/).
  - For Windows: Use the MSI installer.
  - For macOS: Use Homebrew:
    ```bash
    brew install pulumi
    ```
  - For Linux:
    ```bash
    curl -fsSL https://get.pulumi.com | sh
    ```

- **Verify Installation**:
  ```bash
  pulumi version
  ```

### 2.5. Install Boto3

- **Install via pip**:
  ```bash
  pip install boto3
  ```

- **Verify Installation**:
  ```bash
  python -c "import boto3; print(boto3.__version__)"
  ```

---

## 3. Clone the Project Repository

- **Clone the Repository**:
  ```bash
  git clone https://github.com/toharbarazi/Tohar-s-Platform-Engineering-Python-Exercise.git
  cd Tohar-s-Platform-Engineering-Python-Exercise
  ```

---

## 4. Set Up a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

- **Create a Virtual Environment**:
  ```bash
  python -m venv venv
  ```

- **Activate the Virtual Environment**:
  - On Windows:
    ```bash
    .\venv\Scripts\activate
    ```
  - On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

- **Confirm Activation**: Your terminal prompt should now start with `(venv)`.

---

## 5. Install Project Dependencies

**Note**: The repository does not include a `requirements.txt` file. Therefore, you'll need to manually install the necessary dependencies.

- **Install Dependencies**:
  ```bash
  pip install boto3 pulumi
  ```

  If additional dependencies are required based on the project's code, install them similarly.

---

## 6. Configure Pulumi (Detailed)

Pulumi uses the concept of **stacks** to manage different environments (e.g., development, staging, production). Each stack is an isolated instance of your infrastructure configuration.

### 6.1. Log in to Pulumi

First, log in to Pulumi using one of the following methods:
- **Using Pulumi Service (recommended for beginners)**:
  ```bash
  pulumi login
  ```
  This will prompt you to log in using a Pulumi account. If you don’t have one, you can create it for free at [Pulumi.com](https://app.pulumi.com).

- **Using Local File System (if you prefer not to use the Pulumi Service)**:
  ```bash
  pulumi login --local
  ```
  This saves Pulumi state files locally on your machine instead of in the Pulumi Cloud.

---

### 6.2. Initialize a New Stack

Pulumi uses **stacks** to separate different instances of your infrastructure. For example, you might have separate stacks for development (`dev`), staging (`staging`), and production (`prod`).

- **Create a New Stack**:
  ```bash
  pulumi stack init dev
  ```
  In this example, we're creating a stack named `dev`. You can replace `dev` with another name if needed.

- **Explanation**:
  - This command initializes a new instance of the infrastructure defined in your project.
  - A stack stores configuration values, secrets, and state data specific to that instance.
  - You can create multiple stacks to manage different environments.
  
- **Check Existing Stacks**:
  If you're unsure which stacks already exist or want to list all available stacks, use:
  ```bash
  pulumi stack ls
  ```

---

### 6.3. Set Configuration Values

Each stack can have its own configuration values. For this project, you need to specify the AWS region.

- **Set AWS Region**:
  ```bash
  pulumi config set aws:region us-east-1
  ```
  Replace `us-east-1` with your preferred AWS region (e.g., `us-west-2`, `eu-central-1`, etc.).

- **View Configuration Settings**:
  To see all configuration settings for the current stack, use:
  ```bash
  pulumi config
  ```

---

### 6.4. Selecting and Managing Stacks

- **Select a Stack**:
  If you have multiple stacks and want to switch between them:
  ```bash
  pulumi stack select dev
  ```
  Replace `dev` with the name of the stack you want to switch to.

- **Remove a Stack**:
  If you created a stack by mistake or no longer need it:
  ```bash
  pulumi stack rm dev
  ```

---

### 6.5. Running Pulumi Commands

Once the stack is initialized and configured, you can deploy your infrastructure:

- **Preview the Changes**:
  ```bash
  pulumi preview
  ```
  This shows you what changes Pulumi will make to your infrastructure without actually applying them.

- **Apply the Changes**:
  ```bash
  pulumi up
  ```
  This will create the resources defined in your project.

- **Destroy the Stack**:
  If you want to delete all resources created by Pulumi:
  ```bash
  pulumi destroy
  ```

---

### 6.6. Important Notes

- Pulumi relies on the **`__main__.py`** file to define the infrastructure.
- Ensure your virtual environment is activated before running Pulumi commands.
- Make sure your AWS credentials are properly configured using the `aws configure` command.

---

## 7. Important Setup Note !

During the Pulumi setup, an additional `main.py` file might be created automatically. To ensure the CLI functions correctly:

- **Remove the Auto-Generated `main.py`**:
  ```bash
  rm main.py
  ```

- **Ensure the Repository's `__main__.py`** is present and correctly named.

---

# Ready to get started?!

Run the following command in your workspace:

- **Execute the CLI Script**:
  ```bash
  python get_user_input.py
  ```

- **Follow the On-Screen Prompts** to manage your AWS resources.

---

## 9. Additional Tips

- **Deactivating the Virtual Environment**:
  When you're done, you can deactivate the virtual environment by running:
  ```bash
  deactivate
  ```

- **Reactivating the Virtual Environment**:
  Whenever you return to the project, reactivate the virtual environment:
  - On Windows:
    ```bash
    .\venv\Scripts\activate
    ```
  - On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

- **Installing Additional Packages**:
  If you add new Python packages to the project, install them using `pip` and consider creating a `requirements.txt` file for future reference:
  ```bash
  pip install package_name
  pip freeze > requirements.txt
  ```

---

By following these steps, you should have the project set up and running successfully. If you encounter any issues or need further assistance, feel free to ask! 




# Good luck, and thank you for using Tohar's CLI!



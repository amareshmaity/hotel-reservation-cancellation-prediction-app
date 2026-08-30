# !Fix: Service Account Key Creation (Json file) Disabled in Google Cloud

### Problem

When creating a **Service Account Key**, Google Cloud may show an error because **service account key creation is disabled by an Organization Policy**.

The is the solution to grant the required permission and then override the policy **only for the required project**.

<br/>

## Step 1 — Open Google Cloud IAM

1. Sign in to the **Google Cloud Console**.
2. Open the **Project Picker**. (Shortcut to open project picker - Ctrl + o)
3. Click the **three-dot menu** at the top-right.
4. Select **IAM & Permissions**.

**Alternative:** From the Project Picker, select the **root Organization**, then open **IAM** from the left navigation menu.

<br/>

## Step 2 — Grant Organization Policy Administrator Role

1. Click **Grant Access**.
2. In **New principals**, enter your email address (user account email - ama****02.@gmail.com).
3. Under **Assigned roles**, search for:

```text
Organization Policy Administrator
```

4. Select the role.
5. Click **Save**.

This gives your account the required permission to modify the relevant organization policy.

<br/>

## Step 3 — Select the Target Project

First select the `organization policy` tab at left side bar.


1. Open the **Project Picker**.
2. Select the specific project where you need to create the service-account key.

Inside the selected project:

3. In the filter option, search for **iam.disableServiceAccountCreation**.
4. Open the corresponding policy/constraint related to **service account key creation**.
5. Click on `3-dots` and select `edit`.
6. A pop up window will open.

### Note:
It is recommended that **not enabling service-account-key creation at the organization level** unless necessary, Only enable it for the particular project.

Instead:

```text
Organization level → Keep disabled
             ↓
Individual project → Enable only when required
```

<br/>

## Step 4 — Override the Parent Policy

Open the policy and:

1. Select **Override parents policy**.
2. Click **Add a rule**.
3. Set:

```text
Enforcement → Off
```

4. Click **Set Policy**.

This creates a project-level override instead of changing the organization-wide policy.

<br/>

## Step 5 — Create the Service Account Key Again

Return to:

**IAM & Admin → Service Accounts**

1. Open the required service account.
2. Go to **Keys**.
3. Select **Add Key → Create new key**.
4. Choose **JSON**.
5. Click **Create**.



<br/>

## Step 7 — If It Still Fails

Policy changes may take some time to propagate.

If key creation is still failing:

```text
Wait a few minutes
      ↓
Try creating the key again
```



<br/>

### Important security point

It is recommended that **keeping service-account key creation disabled at the organization level** and enabling it only for individual projects when required. This minimizes the scope of the exception and is the safer approach described in the source.

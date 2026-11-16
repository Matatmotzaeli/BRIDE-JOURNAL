# BRIDE JOURNAL – Free App Editorial Admin (development branch)

This feature is **only** for the free app repository `Matatmotzaeli/BRIDE-JOURNAL`.
The catalog and paid SYSTEM repositories are not modified.

## Files
- `admin.html` – login + editorial administration UI with draft, JSON backup, reset and publish controls.
- `admin-defaults.js` – a frozen snapshot of the app's existing editorial defaults, used to populate the editor without touching couple data.
- `index.html` – public app reads published editorial content and falls back to its existing built-in defaults if no document exists or reading is denied.

## Where the manager would sign in (after approval / deployment)
`https://matatmotzaeli.github.io/BRIDE-JOURNAL/admin.html`

**This path is NOT live yet.** GitHub Pages serves `main`; this work is on a development branch.

## Firestore security: REQUIRED before enabling publish

The app stores published editorial content at `siteContent/editorial` in Firebase project `bride-journal`.

The live Firestore rules are NOT stored in this repository and have not been inspected in this work. **Do not deploy a generic rules file or replace current rules**: doing so could break existing account data or weaken security. Before merging, inspect the live rules in Firebase Console and merge a narrowly scoped rule into the EXISTING `rules_version='2'` `service cloud.firestore` / `match /databases/{database}/documents` block:

```
// Example only. Merge with the EXISTING production rules; never deploy alone.
// Use the pre-existing Firebase Auth admin email claim, and verify the admin account exists in this project.
match /siteContent/{documentId} {
  allow get: if documentId == 'editorial';
  allow list: if false;
  allow create, update, delete: if documentId == 'editorial'
    && request.auth != null
    && request.auth.token.email == 'matatmail@gmail.com';
}
```

This example intentionally permits the public app to read ONLY the published editorial document, and restricts writes to the existing admin email as asserted in a Firebase Auth token. Never use `allow write: if true` or rely only on the page's admin login. Do not change user-specific rules.

**Admin sign-in:** `admin.html` currently checks the intended admin email (`matatmail@gmail.com`) on the client. Server-side security MUST additionally enforce the authenticated admin email claim in Firestore rules. The admin's login must exist in the **free-app Firebase Auth project**, not merely the catalog project.

The document contains editorial defaults, not personally identifiable couple data. Public users can read the published content by design.

## What is edited
- Home: seven titles/description strings
- Task seed: text, category, month and notes **for newly seeded accounts only**
- Budget seed: item names and price/tip strings **for newly seeded accounts only**
- Venue questionnaire: question/category/tip text, preserving ordering and number
- Vendor guides: titles, descriptions, video URLs and checklist text
- Venue general advice
- Side-events headings and tab labels
- Public recommendations: title, description, category, link and remote image URL. Direct image-file upload is not yet enabled because the free app has no verified storage configuration. Do not assume Cloudinary's catalog configuration applies to this project.

## Non-destructive behavior
- All personalized user data remains in `users/{uid}/data/*`.
- Published editorial data is shared in `siteContent/editorial`.
- Already-saved user tasks/budget entries are NOT overwritten.
- Question count/order remains unchanged because individual venue answers use numeric indexes.
- Errors when loading editorial content fall back to code defaults.
- Login/registration, Firebase project, and current global CSS remain unchanged.

## Tests before approval
1. Compare the PR against main; ensure no modification to the SYSTEM/catalog repositories.
2. Preview with a test account on a local Cloud Shell web server, NOT the published production site. Do not enter production credentials into third-party HTML preview services.
3. Confirm ordinary users cannot write `siteContent/editorial`; only the authenticated admin email can, once secure rules are configured.
4. Edit a home heading in admin, save draft, reload and restore the draft. Do not publish until rules are configured and approved.
5. Confirm read-only public rendering after publish using a test document, with explicit approval.
6. Confirm existing couples' saved tasks, budget and venue answers are untouched.
7. Verify mobile/table layouts, onboarding, logins and Google sign-in.
8. Direct image uploads require a separate security/storage decision.

## Deployment status
Not deployed or merged. No Firebase backend rules, Auth configuration, or Firestore data have been changed.

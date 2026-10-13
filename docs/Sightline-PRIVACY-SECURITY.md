# Sightline — Privacy and Security Notes

This document records the privacy and security assumptions for the current local development prototype. It is not a formal security audit, legal assessment, or production-readiness approval.

## 1. Current operating model

Sightline currently runs inference through a local FastAPI service and a browser dashboard:

- Dashboard: `http://127.0.0.1:5500`
- API: `http://127.0.0.1:8000`
- Model checkpoint: `models/best.pt`

The dashboard requests webcam access through the browser and sends image frames to the local API for processing. Use the app only with camera access and images you are authorised to use.

## 2. Webcam and image handling

- Start the camera only when you intend to test the application.
- Stop the camera when testing is finished.
- Check the browser's camera-permission indicator and revoke permission in browser settings if needed.
- Avoid showing private documents, messages, other people, or sensitive surroundings in test frames.
- Use sample images you own or have permission to process.
- Do not assume that data is never retained merely because inference is local; verify the actual code and logs before making that claim.
- Before adding cloud inference, analytics, recording, or storage, document what is sent, where it goes, why it is needed, and how long it is retained.

## 3. Model weights and repository hygiene

The custom model is stored at:

`models/best.pt`

The project's `.gitignore` includes `models/*.pt`. Keep this rule unless you intentionally choose a reviewed distribution strategy.

Before publishing code:
- [ ] Confirm model weights are not staged for Git.
- [ ] Confirm no webcam footage, private images, API keys, passwords, or personal data are staged.
- [ ] Review the repository diff and file list before committing.
- [ ] Check the licences and terms for images used in the dataset.
- [ ] Avoid publishing the complete dataset unless redistribution rights are clear.

Useful local Git checks:

```bash
git status --short
git diff --cached --stat
```

If you use Git, inspect staged files before committing. `.gitignore` does not remove a file that Git is already tracking.

## 4. Local network exposure

For the current prototype:
- Keep the API bound to localhost.
- Do not use public tunnels or router port-forwarding to expose the API.
- Do not change CORS to allow every origin as a shortcut.
- Do not assume CORS is authentication; CORS is a browser access control, not a replacement for API security.

The configured dashboard origin is `http://127.0.0.1:5500`. Keep it aligned with the actual dashboard origin used during local development.

## 5. Upload validation and resource limits

Before production use, review the API implementation for:
- Allowed file types and content validation
- Maximum upload size
- Safe image decoding and handling of malformed files
- Clear error responses that do not expose internal paths or stack traces
- Timeouts and resource limits
- Rate limiting and abuse prevention
- Dependency updates and vulnerability review

Do not rely on a filename extension alone to prove an upload is a valid image.

## 6. Frontend and API security

Before deployment:
- Add authentication and authorization if the API should not be available to everyone who can reach it.
- Configure HTTPS for any non-local deployment.
- Restrict CORS to the exact trusted frontend origin(s).
- Keep secrets out of frontend code and source control.
- Avoid logging raw image contents or sensitive request data.
- Add monitoring and safe error handling appropriate to the deployment.
- Test that stopping the camera actually stops frame capture and API requests.

## 7. Dataset licensing and responsible use

Sightline's custom dataset has included images collected through a phone camera and from sources such as Unsplash, Pexels, and Google Images. Availability in a search result does not automatically grant permission to reuse or redistribute an image.

For each image or source group:
- Record the source and retrieval date where practical.
- Check the applicable licence and terms.
- Respect attribution and redistribution requirements.
- Remove images if the licence or consent status is unsuitable.
- Avoid collecting or publishing identifiable people without an appropriate lawful basis and permission where required.

This note is a practical reminder, not legal advice.

## 8. Known boundaries

The current project is a local prototype, not a production surveillance or identity system.

- Tracking IDs are temporary tracker identifiers, not verified identities.
- Detection can fail or misclassify objects.
- A detection result should not be treated as proof of a person's identity, intent, or behaviour.
- Do not use this prototype as the sole basis for consequential decisions about people.
- The hosted static frontend is a presentation layer; it does not itself host the Python inference service.

## 9. Pre-release checklist

Before any public demo or deployment:

- [ ] Decide what data is processed and whether anything is retained.
- [ ] Review camera start/stop behaviour.
- [ ] Review dataset and model distribution rights.
- [ ] Verify model weights and sensitive files are excluded from public Git history.
- [ ] Review API upload validation and size limits.
- [ ] Configure authentication, HTTPS, CORS, and rate limits as appropriate.
- [ ] Test failure cases and safe error handling.
- [ ] Document deployment architecture and privacy notice.
- [ ] Obtain appropriate consent for any people whose images or footage are used.

## 10. Change history

| Date | Change |
|---|---|
| TODO | Initial privacy and security notes created for the local prototype |

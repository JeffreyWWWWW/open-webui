# Nuobao LLM rebrand design

## Goal

White-label the Open WebUI product experience as **Nuobao LLM**. The abbreviated
brand is **NBLLM**. Use the supplied blue infinity-mark image as the default
application logo and icon source.

## Scope

The product-facing default name changes from `Open WebUI` to `Nuobao LLM` in
page titles, authentication, sidebar, About, notifications, metadata and all
localized strings. Product-owned compact or machine-facing labels use `NBLLM`
or `nbllm` when doing so does not change an established public integration
contract.

Default logo, favicon, PWA and splash assets are replaced with derivatives of
the supplied logo. The deployment can still override the name and branding
through its normal configuration, but the stock experience must not append
`(Open WebUI)` to a custom name.

Open WebUI-owned web links, default favicon URLs and remote custom-branding
lookups are removed or made local/configurable. No Nuobao web domain will be
invented: where a replacement destination is not configured, the UI will not
send users to an Open WebUI-owned destination.

## Explicit non-goals

- Do not rename the `open-webui` Python/npm package, Docker image, compose
  service names, database migrations or persisted database keys. These are
  compatibility surfaces, not end-user branding.
- Do not rename functional provider/integration names, including Ollama,
  OpenAI, Google, Microsoft and Jupyter.
- Do not modify upstream license, copyright, contributor agreement or other
  legally required attributions.
- Do not change user data, database schema or runtime behavior apart from the
  branding configuration and removal of outbound upstream-brand links.

## Components and data flow

1. **Backend defaults.** Set `WEBUI_NAME` to `Nuobao LLM`, remove the legacy
   suffixing behavior, and use packaged local branding assets rather than a
   hard-coded Open WebUI favicon URL. Disable the legacy `CUSTOM_NAME` fetch to
   the Open WebUI API.
2. **Frontend text and metadata.** Replace literal Open WebUI product labels
   in runtime TypeScript/Svelte, English source translations and localized
   translation values. Existing dynamic uses of `WEBUI_NAME` continue to
   render the backend-configured value.
3. **External navigation.** Replace product-owned community, documentation,
   model and social links with a locally configured optional `WEBUI_URL` /
   support URL. When absent, omit the link rather than retain the upstream URL.
4. **Assets.** Copy the approved source image into the application asset set
   and generate correctly sized PNG/favicon/PWA/splash derivatives. Preserve
   unrelated user-upload and emoji assets.
5. **Compatibility labels.** User-visible default labels such as CSS classes,
   drag MIME types and optional request-header defaults may move to `nbllm`
   only where all first-party producers and consumers are updated together.
   Existing legacy identifiers remain accepted when practical.

## Error handling and security

Missing optional support URLs must not create broken links. Missing local logo
assets must fall back to the packaged favicon rather than an external resource.
No branding setting may require a request to an external Open WebUI service.

## Verification

- Static scans confirm runtime/product-facing occurrences of `Open WebUI`,
  `OpenWebUI` and `openwebui.com` are either absent, intentionally preserved
  for legal attribution, or listed as compatibility-only.
- Validate the main HTML metadata, login screen, sidebar and About screen with
  `Nuobao LLM` as the default and with an administrator override.
- Confirm the supplied logo renders as the favicon, PWA icon and splash asset.
- Run formatting/type checking/build tests available in the repository.
- Review the final diff to ensure provider names and legal notices were not
  renamed accidentally.

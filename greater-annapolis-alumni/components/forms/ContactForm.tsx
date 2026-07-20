"use client";

import { FormEvent, useId, useState } from "react";

type Status = "idle" | "success" | "error";

const inquiryTypes = [
  "General question",
  "Membership",
  "Scholarships",
  "Events",
  "Community service",
  "Media / partnership",
  "Other",
];

/**
 * Staging-safe contact form. Validates required fields client-side and
 * shows success/error states, but does not send email anywhere — see
 * the note above the submit button. Includes a honeypot field as a
 * placeholder for spam protection; replace with a real service
 * (reCAPTCHA, hCaptcha, Turnstile) before production launch.
 */
export function ContactForm() {
  const [status, setStatus] = useState<Status>("idle");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const nameId = useId();
  const emailId = useId();
  const phoneId = useId();
  const typeId = useId();
  const messageId = useId();

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);

    // Honeypot: real users never fill this hidden field in.
    if (String(formData.get("company") ?? "").length > 0) {
      setStatus("success");
      form.reset();
      return;
    }

    const name = String(formData.get("name") ?? "").trim();
    const email = String(formData.get("email") ?? "").trim();
    const inquiryType = String(formData.get("inquiryType") ?? "").trim();
    const message = String(formData.get("message") ?? "").trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    const nextErrors: Record<string, string> = {};
    if (!name) nextErrors.name = "Enter your name.";
    if (!emailPattern.test(email)) nextErrors.email = "Enter a valid email address.";
    if (!inquiryType) nextErrors.inquiryType = "Choose an inquiry type.";
    if (!message) nextErrors.message = "Enter a message.";

    if (Object.keys(nextErrors).length > 0) {
      setErrors(nextErrors);
      setStatus("error");
      return;
    }

    setErrors({});
    setStatus("success");
    form.reset();
  }

  return (
    <form onSubmit={handleSubmit} noValidate className="space-y-5">
      {/* Honeypot field: hidden from sighted and screen-reader users, but bots often fill every field. */}
      <div className="hidden" aria-hidden="true">
        <label htmlFor="company">Company</label>
        <input id="company" name="company" type="text" tabIndex={-1} autoComplete="off" />
      </div>

      <div>
        <label htmlFor={nameId} className="block text-sm font-semibold text-black">
          Name
        </label>
        <input
          id={nameId}
          name="name"
          type="text"
          required
          aria-invalid={Boolean(errors.name)}
          aria-describedby={errors.name ? `${nameId}-error` : undefined}
          className="mt-1 w-full rounded-md border border-gray/40 px-3 py-2 text-sm text-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-maroon"
        />
        {errors.name && (
          <p id={`${nameId}-error`} role="alert" className="mt-1 text-sm font-semibold text-maroon">
            {errors.name}
          </p>
        )}
      </div>

      <div>
        <label htmlFor={emailId} className="block text-sm font-semibold text-black">
          Email
        </label>
        <input
          id={emailId}
          name="email"
          type="email"
          required
          aria-invalid={Boolean(errors.email)}
          aria-describedby={errors.email ? `${emailId}-error` : undefined}
          className="mt-1 w-full rounded-md border border-gray/40 px-3 py-2 text-sm text-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-maroon"
        />
        {errors.email && (
          <p id={`${emailId}-error`} role="alert" className="mt-1 text-sm font-semibold text-maroon">
            {errors.email}
          </p>
        )}
      </div>

      <div>
        <label htmlFor={phoneId} className="block text-sm font-semibold text-black">
          Phone <span className="font-normal text-black/60">(optional)</span>
        </label>
        <input
          id={phoneId}
          name="phone"
          type="tel"
          className="mt-1 w-full rounded-md border border-gray/40 px-3 py-2 text-sm text-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-maroon"
        />
      </div>

      <div>
        <label htmlFor={typeId} className="block text-sm font-semibold text-black">
          Inquiry Type
        </label>
        <select
          id={typeId}
          name="inquiryType"
          required
          defaultValue=""
          aria-invalid={Boolean(errors.inquiryType)}
          aria-describedby={errors.inquiryType ? `${typeId}-error` : undefined}
          className="mt-1 w-full rounded-md border border-gray/40 bg-white px-3 py-2 text-sm text-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-maroon"
        >
          <option value="" disabled>
            Choose one&hellip;
          </option>
          {inquiryTypes.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
        {errors.inquiryType && (
          <p id={`${typeId}-error`} role="alert" className="mt-1 text-sm font-semibold text-maroon">
            {errors.inquiryType}
          </p>
        )}
      </div>

      <div>
        <label htmlFor={messageId} className="block text-sm font-semibold text-black">
          Message
        </label>
        <textarea
          id={messageId}
          name="message"
          required
          rows={5}
          aria-invalid={Boolean(errors.message)}
          aria-describedby={errors.message ? `${messageId}-error` : undefined}
          className="mt-1 w-full rounded-md border border-gray/40 px-3 py-2 text-sm text-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-maroon"
        />
        {errors.message && (
          <p id={`${messageId}-error`} role="alert" className="mt-1 text-sm font-semibold text-maroon">
            {errors.message}
          </p>
        )}
      </div>

      <p className="text-xs text-black/60">
        Staging preview: this form does not send a live email. It will be connected to the
        chapter&rsquo;s real contact address before production launch.
      </p>

      <button type="submit" className="btn-primary">
        Send Message
      </button>

      {status === "success" && (
        <p role="status" className="rounded-md bg-maroon/10 px-4 py-3 text-sm font-semibold text-maroon">
          Message received (staging preview only — no email was sent). Thank you for reaching out.
        </p>
      )}
      {status === "error" && (
        <p role="alert" className="rounded-md bg-black/5 px-4 py-3 text-sm font-semibold text-black">
          Please fix the highlighted fields and try again.
        </p>
      )}
    </form>
  );
}

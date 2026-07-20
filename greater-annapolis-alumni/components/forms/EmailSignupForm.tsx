"use client";

import { FormEvent, useId, useState } from "react";

type Status = "idle" | "success" | "error";

/**
 * Staging-safe email signup form. No email is sent — this only
 * validates input and shows a success state, so the chapter can review
 * the UX before a real signup provider (e.g. Mailchimp) is connected.
 */
export function EmailSignupForm() {
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState<string | null>(null);
  const inputId = useId();
  const errorId = useId();

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const email = String(formData.get("email") ?? "").trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email)) {
      setError("Enter a valid email address.");
      setStatus("error");
      return;
    }

    setError(null);
    setStatus("success");
    event.currentTarget.reset();
  }

  return (
    <form className="mt-4" onSubmit={handleSubmit} noValidate>
      <label htmlFor={inputId} className="block text-sm font-semibold text-black">
        Email address
      </label>
      <div className="mt-2 flex flex-col gap-3 sm:flex-row">
        <input
          id={inputId}
          name="email"
          type="email"
          required
          aria-invalid={status === "error"}
          aria-describedby={status === "error" ? errorId : undefined}
          placeholder="you@example.com"
          className="w-full rounded-md border border-gray/40 px-3 py-2 text-sm text-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-maroon"
        />
        <button type="submit" className="btn-primary shrink-0">
          Sign Up
        </button>
      </div>
      {status === "error" && (
        <p id={errorId} role="alert" className="mt-2 text-sm font-semibold text-maroon">
          {error}
        </p>
      )}
      {status === "success" && (
        <p role="status" className="mt-2 text-sm font-semibold text-maroon">
          Thanks — your email was captured for this staging preview only (no message was actually sent).
        </p>
      )}
    </form>
  );
}

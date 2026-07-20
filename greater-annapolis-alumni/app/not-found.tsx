import Link from "next/link";
import { Container } from "@/components/ui/Container";

export default function NotFound() {
  return (
    <section className="section bg-white">
      <Container className="flex flex-col items-center py-20 text-center">
        <p className="eyebrow">404</p>
        <h1 className="mt-2 text-3xl font-bold text-black sm:text-4xl">Page Not Found</h1>
        <p className="mt-4 max-w-md text-black/70">
          The page you&rsquo;re looking for doesn&rsquo;t exist or may have moved. Let&rsquo;s get
          you back on track.
        </p>
        <Link href="/" className="btn-primary mt-8">
          Return Home
        </Link>
      </Container>
    </section>
  );
}

import { Container } from "@/components/Container";

export function PolicyPage({
  title,
  updatedAt,
  sections,
}: {
  title: string;
  updatedAt: string;
  sections: { heading: string; body: string[] }[];
}) {
  return (
    <div className="bg-ivory-50 py-16">
      <Container className="max-w-2xl">
        <div className="mb-10 flex flex-col gap-2">
          <h1 className="font-serif-kr text-2xl font-medium text-navy-900 sm:text-3xl">
            {title}
          </h1>
          <p className="text-sm text-warmgray-500">시행일: {updatedAt}</p>
        </div>
        <div className="flex flex-col gap-10">
          {sections.map((s) => (
            <div key={s.heading} className="flex flex-col gap-3">
              <h2 className="text-lg font-semibold text-navy-900">{s.heading}</h2>
              {s.body.map((p, i) => (
                <p key={i} className="leading-relaxed whitespace-pre-line text-warmgray-700">
                  {p}
                </p>
              ))}
            </div>
          ))}
        </div>
      </Container>
    </div>
  );
}

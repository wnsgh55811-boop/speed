"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { clsx } from "clsx";

export function Accordion({
  items,
}: {
  items: { question: string; answer: string }[];
}) {
  const [open, setOpen] = useState<number | null>(0);

  return (
    <div className="flex flex-col gap-3">
      {items.map((item, i) => {
        const isOpen = open === i;
        return (
          <div
            key={item.question}
            className="rounded-sm border border-warmgray-200 bg-white"
          >
            <button
              className="flex w-full items-center justify-between gap-4 px-6 py-5 text-left"
              onClick={() => setOpen(isOpen ? null : i)}
            >
              <span className="font-medium text-navy-900">
                <span className="mr-2 text-burgundy-700">Q.</span>
                {item.question}
              </span>
              <ChevronDown
                size={18}
                className={clsx(
                  "shrink-0 text-warmgray-500 transition-transform",
                  isOpen && "rotate-180",
                )}
              />
            </button>
            {isOpen && (
              <div className="border-t border-warmgray-200 px-6 py-5 leading-relaxed text-warmgray-700">
                <span className="mr-2 font-medium text-navy-900">A.</span>
                {item.answer}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

"use client"

import { Input } from "../components/ui/input"
import { JSX, SVGProps } from "react"

function SearchIcon(props: JSX.IntrinsicAttributes & SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.3-4.3" />
    </svg>
  )
}

export function SearchBar() {
  return (
    <form className="relative">
      <SearchIcon className="absolute left-2 top-1/2 -translate-y-1/2 text-muted-foreground h-4 w-4" />
      <Input
        type="search"
        placeholder={"Search..."}
        className="pl-8 bg-background text-foreground text-sm focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 w-24 md:w-56"
      />
    </form>
  )
}
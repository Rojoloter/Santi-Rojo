"use client"

import { type LucideIcon } from "lucide-react"

import {
  SidebarGroup,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "../components/ui/sidebar"

export function NavProjects({
  projects,
  onCategoryClick,
}: {
  projects: {
    name: string
    url: string
    icon: LucideIcon
  }[]
  onCategoryClick?: (category: string) => void
}) {
  useSidebar()

  return (
    <SidebarGroup>
      <SidebarMenu>
        {projects.map((item) => (
          <SidebarMenuItem key={item.name}>
            <SidebarMenuButton asChild>
              <a 
                href={item.url} 
                onClick={(e) => {
                  e.preventDefault();
                  onCategoryClick?.(item.name);
                }}
              >
                <item.icon />
                <span>{item.name}</span>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        ))} 
      </SidebarMenu>
    </SidebarGroup>
  )
}

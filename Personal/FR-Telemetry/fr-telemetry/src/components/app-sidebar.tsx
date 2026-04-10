"use client"

import * as React from "react"
import {
  GaugeIcon,
  CarIcon,
  HomeIcon,
  InfoIcon,
} from "lucide-react"

import { NavMain } from "../components/nav-main"
import { NavProjects } from "../components/nav-projects"
import { SidebarBrand } from "../components/sidebar-brand"
import { SidebarBottom } from "../components/sidebar-bottom"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "../components/ui/sidebar"

const data = {
  brand: {
    name: "FIUBA Racing",
    logo: "/fiuba-racing-logo.png",
  },
  university: {
    title: "FIUBA",
    subtitle: "Formula SAE",
    year: "2025 - 2026",
    logo: "/fiuba-logo.png",
  },
  home: [
    {
      name: "Home",
      url: "#",
      icon: HomeIcon,
    },
  ],
  navMain: [
    {
      title: "Piloto",
      url: "#",
      icon: GaugeIcon,
      items: [
        {
          title: "TPS & Freno",
          url: "#",
        },
        {
          title: "Velocidad & RPM",
          url: "#",
        },
        {
          title: "Posición del Volante",
          url: "#",
        },
      ],
    },
    {
      title: "Auto",
      url: "#",
      icon: CarIcon,
      items: [
        {
          title: "Motor",
          url: "#",
        },
        {
          title: "Aceleraciones",
          url: "#",
        },
        {
          title: "Fuerzas",
          url: "#",
        },
        {
          title: "Desplazamientos",
          url: "#",
        },
        {
          title: "Neumáticos",
          url: "#",
        },
      ],
    },
  ],
  about: [
    {
      name: "About",
      url: "#",
      icon: InfoIcon,
    },
  ],
}

export function AppSidebar({ onCategoryClick, ...props }: React.ComponentProps<typeof Sidebar> & { onCategoryClick?: (category: string) => void }) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <SidebarBrand brand={data.brand} />
      </SidebarHeader>
      <SidebarContent>
        <NavProjects projects={data.home} onCategoryClick={onCategoryClick}/>
        <NavMain items={data.navMain} onCategoryClick={onCategoryClick}/>
        <NavProjects projects={data.about} onCategoryClick={onCategoryClick}/>
      </SidebarContent>
      <SidebarFooter>
        <SidebarBottom detail={data.university} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}

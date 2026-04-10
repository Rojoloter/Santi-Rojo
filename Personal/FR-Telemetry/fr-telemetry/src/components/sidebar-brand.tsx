import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "./ui/sidebar"

interface SidebarBrandProps {
  brand: {
    name: string
    logo: string
  }
}

export function SidebarBrand({ brand }: SidebarBrandProps) {
  const { state } = useSidebar()

  const BrandLink = ({ children }: { children: React.ReactNode }) => {
    return <a href="#" onClick={(e) => e.preventDefault()}>{children}</a>
  }

  const isExpanded = state === "expanded"

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <BrandLink>
          <SidebarMenuButton
            size="lg"
            className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground h-18 justify-center"
          >
            <div className={`bg-sidebar-primary dark:bg-background text-sidebar-primary-foreground flex items-center justify-center rounded-lg transition-all duration-300 overflow-hidden ${isExpanded ? "h-16 w-58" : "h-8 w-8"}`}>
              <img
                src={brand.logo}
                alt={brand.name}
                className={
                  isExpanded
                    ? "object-contain h-20 w-80"
                    : "object-contain h-8 w-8"
                }
              />
            </div>
          </SidebarMenuButton>
        </BrandLink>
      </SidebarMenuItem>
    </SidebarMenu>
  )
}
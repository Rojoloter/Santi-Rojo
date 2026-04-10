import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "./ui/sidebar"

interface SidebarBottomProps {
  detail: {
    title: string
    subtitle: string
    year: string
    logo: string
  }
}

export function SidebarBottom({ detail }: SidebarBottomProps) {
  const { state } = useSidebar()

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <a href="https://fi.uba.ar" target="_blank" rel="noopener noreferrer">
          <SidebarMenuButton
            size="lg"
            className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground h-16"
          >
            <div className="flex items-center gap-2 w-full">
              <div className={`rounded-full overflow-hidden bg-white flex items-center justify-center transition-all duration-300 ${
                state === "expanded" ? "h-12 w-12" : "h-8 w-8"
              }`}>
                <img
                  src={detail.logo}
                  alt={detail.title}
                  width={state === "expanded" ? 48 : 32}
                  height={state === "expanded" ? 48 : 32}
                  className="object-cover"
                />
              </div>
              {state === "expanded" && (
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span
                    className="truncate font-medium text-sm"
                    style={{ fontFamily: "Formula1-Display-Bold, sans-serif" }}
                  >
                    {detail.title}
                  </span>
                  <span
                    className="truncate font-normal text-xs"
                    style={{ fontFamily: "Formula1-Display-Regular, sans-serif" }}
                  >
                    {detail.subtitle}
                  </span>
                  <span
                    className="truncate font-normal text-sm ml-0.5"
                    style={{ fontFamily: "Formula1-Display-Year, sans-serif" }}
                  >
                    {detail.year}
                  </span>
                </div>
              )}
            </div>
          </SidebarMenuButton>
        </a>
      </SidebarMenuItem>
    </SidebarMenu>
  )
}
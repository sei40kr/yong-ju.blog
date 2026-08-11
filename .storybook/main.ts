import type { StorybookConfig } from "@storybook/nextjs-vite";

const config: StorybookConfig = {
  // Stories live next to the component they document.
  stories: ["../src/**/*.stories.@(ts|tsx)"],
  addons: ["@storybook/addon-a11y", "@storybook/addon-docs"],
  framework: "@storybook/nextjs-vite",
  staticDirs: ["../public"],
  core: { disableTelemetry: true },
};

export default config;

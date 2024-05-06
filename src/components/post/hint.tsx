import { component$, Slot } from "@builder.io/qwik";
import { BsInfoCircle } from "@qwikest/icons/bootstrap";
import { css } from "~/styled-system/css";
import { HStack } from "~/styled-system/jsx";

export const Hint = component$(
	({ level }: { level: "info" | "warn" | "danger" }) => {
		const wrapperBaseClassName = css({
			my: "4",
			pl: "4",
			pr: "6",
			py: "3",
			borderWidth: "1px",
			borderColor: "gray.200",
			borderLeftWidth: "4px",
			rounded: "lg",
			shadow: "sm",
		});
		const wrapperVariantClassNames = {
			info: css({
				borderLeftColor: "sky.600",
			}),
			warn: css({
				borderLeftColor: "amber.600",
			}),
			danger: css({
				borderLeftColor: "rose.600",
			}),
		};
		const iconVariantClassNames = {
			info: css({
				color: "sky.600",
			}),
			warn: css({
				color: "amber.600",
			}),
			danger: css({
				color: "rose.600",
			}),
		};
		return (
			<div class={`${wrapperBaseClassName} ${wrapperVariantClassNames[level]}`}>
				<HStack gap="6">
					<div class={iconVariantClassNames[level]}>
						<BsInfoCircle />
					</div>
					<div
						class={css({
							"& > *": {
								_last: { mb: "0" },
							},
						})}
					>
						<Slot />
					</div>
				</HStack>
			</div>
		);
	},
);

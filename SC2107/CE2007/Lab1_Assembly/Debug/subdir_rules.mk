################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

# Each subdirectory must supply rules for building sources it contributes
%.obj: ../%.asm $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: MSP432 Compiler'
	"C:/ti/ccs2020/ccs/tools/compiler/bin/armcl" -mv7M4 --code_state=16 --float_support=FPv4SPD16 -me --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include" --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include/CMSIS" --include_path="C:/Jon/Uni stuff/CE/Embedded-Systems/SC2107/CE2007/Lab1_Assembly" --include_path="C:/ti/ccs2020/ccs/tools/compiler/include" --advice:power=all --define=__MSP432P401R__ --define=ccs -g --gcc --diag_warning=225 --diag_wrap=off --display_error_number --abi=eabi --preproc_with_compile --preproc_dependency="$(basename $(<F)).d_raw" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

%.obj: ../%.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: MSP432 Compiler'
	"C:/ti/ccs2020/ccs/tools/compiler/bin/armcl" -mv7M4 --code_state=16 --float_support=FPv4SPD16 -me --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include" --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include/CMSIS" --include_path="C:/Jon/Uni stuff/CE/Embedded-Systems/SC2107/CE2007/Lab1_Assembly" --include_path="C:/ti/ccs2020/ccs/tools/compiler/include" --advice:power=all --define=__MSP432P401R__ --define=ccs -g --gcc --diag_warning=225 --diag_wrap=off --display_error_number --abi=eabi --preproc_with_compile --preproc_dependency="$(basename $(<F)).d_raw" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '



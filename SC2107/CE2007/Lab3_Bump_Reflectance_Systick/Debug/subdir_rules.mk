################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

# Each subdirectory must supply rules for building sources it contributes
Bump.obj: C:/Jon/Uni\ stuff/CE/Embedded-Systems/SC2107/CE2007/inc/Bump.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: MSP432 Compiler'
	"C:/ti/ccs2020/ccs/tools/compiler/bin/armcl" -mv7M4 --code_state=16 --float_support=FPv4SPD16 -me --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include" --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include/CMSIS" --include_path="C:/Jon/Uni stuff/CE/Embedded-Systems/SC2107/CE2007/Lab3_Bump_Reflectance_Systick" --include_path="C:/ti/ccs2020/ccs/tools/compiler/include" --advice:power=all --define=__MSP432P401R__ --define=ccs -g --c99 --gcc --diag_warning=225 --diag_wrap=off --display_error_number --abi=eabi --preproc_with_compile --preproc_dependency="Bump.d_raw" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

Clock.obj: C:/Jon/Uni\ stuff/CE/Embedded-Systems/SC2107/CE2007/inc/Clock.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: MSP432 Compiler'
	"C:/ti/ccs2020/ccs/tools/compiler/bin/armcl" -mv7M4 --code_state=16 --float_support=FPv4SPD16 -me --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include" --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include/CMSIS" --include_path="C:/Jon/Uni stuff/CE/Embedded-Systems/SC2107/CE2007/Lab3_Bump_Reflectance_Systick" --include_path="C:/ti/ccs2020/ccs/tools/compiler/include" --advice:power=all --define=__MSP432P401R__ --define=ccs -g --c99 --gcc --diag_warning=225 --diag_wrap=off --display_error_number --abi=eabi --preproc_with_compile --preproc_dependency="Clock.d_raw" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

CortexM.obj: C:/Jon/Uni\ stuff/CE/Embedded-Systems/SC2107/CE2007/inc/CortexM.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: MSP432 Compiler'
	"C:/ti/ccs2020/ccs/tools/compiler/bin/armcl" -mv7M4 --code_state=16 --float_support=FPv4SPD16 -me --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include" --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include/CMSIS" --include_path="C:/Jon/Uni stuff/CE/Embedded-Systems/SC2107/CE2007/Lab3_Bump_Reflectance_Systick" --include_path="C:/ti/ccs2020/ccs/tools/compiler/include" --advice:power=all --define=__MSP432P401R__ --define=ccs -g --c99 --gcc --diag_warning=225 --diag_wrap=off --display_error_number --abi=eabi --preproc_with_compile --preproc_dependency="CortexM.d_raw" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

%.obj: ../%.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: MSP432 Compiler'
	"C:/ti/ccs2020/ccs/tools/compiler/bin/armcl" -mv7M4 --code_state=16 --float_support=FPv4SPD16 -me --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include" --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include/CMSIS" --include_path="C:/Jon/Uni stuff/CE/Embedded-Systems/SC2107/CE2007/Lab3_Bump_Reflectance_Systick" --include_path="C:/ti/ccs2020/ccs/tools/compiler/include" --advice:power=all --define=__MSP432P401R__ --define=ccs -g --c99 --gcc --diag_warning=225 --diag_wrap=off --display_error_number --abi=eabi --preproc_with_compile --preproc_dependency="$(basename $(<F)).d_raw" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

LaunchPad.obj: C:/Jon/Uni\ stuff/CE/Embedded-Systems/SC2107/CE2007/inc/LaunchPad.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: MSP432 Compiler'
	"C:/ti/ccs2020/ccs/tools/compiler/bin/armcl" -mv7M4 --code_state=16 --float_support=FPv4SPD16 -me --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include" --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include/CMSIS" --include_path="C:/Jon/Uni stuff/CE/Embedded-Systems/SC2107/CE2007/Lab3_Bump_Reflectance_Systick" --include_path="C:/ti/ccs2020/ccs/tools/compiler/include" --advice:power=all --define=__MSP432P401R__ --define=ccs -g --c99 --gcc --diag_warning=225 --diag_wrap=off --display_error_number --abi=eabi --preproc_with_compile --preproc_dependency="LaunchPad.d_raw" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

Reflectance.obj: C:/Jon/Uni\ stuff/CE/Embedded-Systems/SC2107/CE2007/inc/Reflectance.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: MSP432 Compiler'
	"C:/ti/ccs2020/ccs/tools/compiler/bin/armcl" -mv7M4 --code_state=16 --float_support=FPv4SPD16 -me --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include" --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include/CMSIS" --include_path="C:/Jon/Uni stuff/CE/Embedded-Systems/SC2107/CE2007/Lab3_Bump_Reflectance_Systick" --include_path="C:/ti/ccs2020/ccs/tools/compiler/include" --advice:power=all --define=__MSP432P401R__ --define=ccs -g --c99 --gcc --diag_warning=225 --diag_wrap=off --display_error_number --abi=eabi --preproc_with_compile --preproc_dependency="Reflectance.d_raw" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

SysTickInts.obj: C:/Jon/Uni\ stuff/CE/Embedded-Systems/SC2107/CE2007/inc/SysTickInts.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: MSP432 Compiler'
	"C:/ti/ccs2020/ccs/tools/compiler/bin/armcl" -mv7M4 --code_state=16 --float_support=FPv4SPD16 -me --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include" --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include/CMSIS" --include_path="C:/Jon/Uni stuff/CE/Embedded-Systems/SC2107/CE2007/Lab3_Bump_Reflectance_Systick" --include_path="C:/ti/ccs2020/ccs/tools/compiler/include" --advice:power=all --define=__MSP432P401R__ --define=ccs -g --c99 --gcc --diag_warning=225 --diag_wrap=off --display_error_number --abi=eabi --preproc_with_compile --preproc_dependency="SysTickInts.d_raw" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

TExaS.obj: C:/Jon/Uni\ stuff/CE/Embedded-Systems/SC2107/CE2007/inc/TExaS.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: MSP432 Compiler'
	"C:/ti/ccs2020/ccs/tools/compiler/bin/armcl" -mv7M4 --code_state=16 --float_support=FPv4SPD16 -me --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include" --include_path="C:/ti/ccs2020/ccs/ccs_base/arm/include/CMSIS" --include_path="C:/Jon/Uni stuff/CE/Embedded-Systems/SC2107/CE2007/Lab3_Bump_Reflectance_Systick" --include_path="C:/ti/ccs2020/ccs/tools/compiler/include" --advice:power=all --define=__MSP432P401R__ --define=ccs -g --c99 --gcc --diag_warning=225 --diag_wrap=off --display_error_number --abi=eabi --preproc_with_compile --preproc_dependency="TExaS.d_raw" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '



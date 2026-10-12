	.file	"k.c"
	.text
	.p2align 4
	.globl	t8
	.type	t8, @function
t8:
.LFB3:
	.cfi_startproc
	endbr64
	testq	%rsi, %rsi
	je	.L25
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	leaq	-1(%rsi), %rax
	movq	%rdi, %rcx
	leaq	0(,%rsi,8), %rdx
	movq	%rsi, %rdi
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	.cfi_offset 14, -24
	.cfi_offset 13, -32
	.cfi_offset 12, -40
	.cfi_offset 3, -48
	cmpq	$2, %rax
	jbe	.L8
	leaq	(%rcx,%rdx), %rbx
	movq	%rdi, %r13
	xorl	%eax, %eax
	leaq	(%rbx,%rdx), %r11
	shrq	$2, %r13
	leaq	(%r11,%rdx), %r10
	salq	$5, %r13
	leaq	(%r10,%rdx), %r9
	leaq	(%r9,%rdx), %r8
	leaq	(%r8,%rdx), %rsi
	leaq	(%rsi,%rdx), %r12
	.p2align 4,,10
	.p2align 3
.L4:
	vmovupd	(%r11,%rax), %ymm6
	vmovupd	(%rcx,%rax), %ymm1
	vaddpd	(%r10,%rax), %ymm6, %ymm7
	vsubpd	(%r10,%rax), %ymm6, %ymm4
	vsubpd	(%rbx,%rax), %ymm1, %ymm0
	vmovupd	(%rbx,%rax), %ymm5
	vmovupd	(%r9,%rax), %ymm1
	vaddpd	(%rcx,%rax), %ymm5, %ymm5
	vaddpd	(%r8,%rax), %ymm1, %ymm2
	vmovupd	(%rsi,%rax), %ymm6
	vaddpd	(%r12,%rax), %ymm6, %ymm6
	vmovupd	(%rsi,%rax), %ymm3
	vaddpd	%ymm4, %ymm0, %ymm8
	vsubpd	(%r12,%rax), %ymm3, %ymm3
	vsubpd	(%r8,%rax), %ymm1, %ymm1
	vaddpd	%ymm7, %ymm5, %ymm9
	vsubpd	%ymm7, %ymm5, %ymm5
	vaddpd	%ymm6, %ymm2, %ymm7
	vsubpd	%ymm6, %ymm2, %ymm2
	vaddpd	%ymm3, %ymm1, %ymm6
	vsubpd	%ymm3, %ymm1, %ymm1
	vsubpd	%ymm4, %ymm0, %ymm0
	vaddpd	%ymm7, %ymm9, %ymm3
	vsubpd	%ymm7, %ymm9, %ymm4
	vmovupd	%ymm3, (%rcx,%rax)
	vaddpd	%ymm6, %ymm8, %ymm3
	vmovupd	%ymm4, (%r9,%rax)
	vmovupd	%ymm3, (%rbx,%rax)
	vaddpd	%ymm2, %ymm5, %ymm3
	vsubpd	%ymm2, %ymm5, %ymm2
	vmovupd	%ymm3, (%r11,%rax)
	vaddpd	%ymm1, %ymm0, %ymm3
	vsubpd	%ymm1, %ymm0, %ymm0
	vmovupd	%ymm2, (%rsi,%rax)
	vmovupd	%ymm3, (%r10,%rax)
	vsubpd	%ymm6, %ymm8, %ymm3
	vmovupd	%ymm0, (%r12,%rax)
	vmovupd	%ymm3, (%r8,%rax)
	addq	$32, %rax
	cmpq	%r13, %rax
	jne	.L4
	movq	%rdi, %rax
	andq	$-4, %rax
	testb	$3, %dil
	je	.L29
	vzeroupper
.L3:
	movq	%rdi, %r8
	subq	%rax, %r8
	cmpq	$1, %r8
	je	.L6
	leaq	(%rdi,%rax), %rsi
	leaq	(%rcx,%rax,8), %r10
	leaq	(%rcx,%rsi,8), %r9
	addq	%rdi, %rsi
	vmovupd	(%r10), %xmm7
	leaq	(%rcx,%rsi,8), %r11
	addq	%rdi, %rsi
	vmovupd	(%r9), %xmm4
	leaq	(%rcx,%rsi,8), %rbx
	addq	%rdi, %rsi
	vmovupd	(%r11), %xmm0
	leaq	(%rcx,%rsi,8), %r12
	addq	%rdi, %rsi
	vmovupd	(%rbx), %xmm2
	vaddpd	%xmm4, %xmm7, %xmm5
	leaq	(%rcx,%rsi,8), %r13
	addq	%rdi, %rsi
	vmovupd	(%r12), %xmm1
	vsubpd	%xmm4, %xmm7, %xmm7
	leaq	(%rcx,%rsi,8), %r14
	addq	%rdi, %rsi
	vmovupd	0(%r13), %xmm6
	vaddpd	%xmm2, %xmm0, %xmm4
	leaq	(%rcx,%rsi,8), %rsi
	vmovupd	(%r14), %xmm3
	vsubpd	%xmm2, %xmm0, %xmm0
	vmovupd	(%rsi), %xmm8
	vaddpd	%xmm6, %xmm1, %xmm2
	vsubpd	%xmm6, %xmm1, %xmm1
	vaddpd	%xmm8, %xmm3, %xmm6
	vsubpd	%xmm8, %xmm3, %xmm3
	vaddpd	%xmm4, %xmm5, %xmm8
	vsubpd	%xmm4, %xmm5, %xmm4
	vaddpd	%xmm0, %xmm7, %xmm5
	vsubpd	%xmm0, %xmm7, %xmm0
	vaddpd	%xmm6, %xmm2, %xmm7
	vsubpd	%xmm6, %xmm2, %xmm2
	vaddpd	%xmm3, %xmm1, %xmm6
	vsubpd	%xmm3, %xmm1, %xmm1
	vaddpd	%xmm7, %xmm8, %xmm3
	vmovupd	%xmm3, (%r10)
	vaddpd	%xmm6, %xmm5, %xmm3
	vsubpd	%xmm6, %xmm5, %xmm5
	vmovupd	%xmm3, (%r9)
	vaddpd	%xmm2, %xmm4, %xmm3
	vsubpd	%xmm2, %xmm4, %xmm4
	vmovupd	%xmm5, 0(%r13)
	vmovupd	%xmm3, (%r11)
	vaddpd	%xmm1, %xmm0, %xmm3
	vsubpd	%xmm1, %xmm0, %xmm0
	vmovupd	%xmm4, (%r14)
	vmovupd	%xmm3, (%rbx)
	vsubpd	%xmm7, %xmm8, %xmm3
	vmovupd	%xmm0, (%rsi)
	vmovupd	%xmm3, (%r12)
	testb	$1, %r8b
	je	.L23
	andq	$-2, %r8
	addq	%r8, %rax
.L6:
	salq	$3, %rax
	leaq	(%rcx,%rax), %r8
	addq	%rdx, %rax
	leaq	(%rcx,%rax), %r9
	addq	%rdx, %rax
	vmovsd	(%r8), %xmm7
	leaq	(%rcx,%rax), %r10
	addq	%rdx, %rax
	vmovsd	(%r9), %xmm4
	leaq	(%rcx,%rax), %r11
	addq	%rdx, %rax
	vmovsd	(%r10), %xmm0
	leaq	(%rcx,%rax), %rbx
	addq	%rdx, %rax
	vmovsd	(%r11), %xmm2
	vaddsd	%xmm4, %xmm7, %xmm5
	leaq	(%rcx,%rax), %rdi
	addq	%rdx, %rax
	vmovsd	(%rbx), %xmm1
	vsubsd	%xmm4, %xmm7, %xmm7
	addq	%rax, %rdx
	leaq	(%rcx,%rax), %rsi
	vmovsd	(%rdi), %xmm6
	vaddsd	%xmm2, %xmm0, %xmm4
	addq	%rcx, %rdx
	vmovsd	(%rsi), %xmm3
	vsubsd	%xmm2, %xmm0, %xmm0
	vmovsd	(%rdx), %xmm8
	vaddsd	%xmm6, %xmm1, %xmm2
	vsubsd	%xmm6, %xmm1, %xmm1
	vaddsd	%xmm8, %xmm3, %xmm6
	vsubsd	%xmm8, %xmm3, %xmm3
	vaddsd	%xmm4, %xmm5, %xmm8
	vsubsd	%xmm4, %xmm5, %xmm4
	vaddsd	%xmm0, %xmm7, %xmm5
	vsubsd	%xmm0, %xmm7, %xmm0
	vaddsd	%xmm6, %xmm2, %xmm7
	vsubsd	%xmm6, %xmm2, %xmm2
	vaddsd	%xmm3, %xmm1, %xmm6
	vsubsd	%xmm3, %xmm1, %xmm1
	vaddsd	%xmm7, %xmm8, %xmm3
	vsubsd	%xmm7, %xmm8, %xmm7
	vmovsd	%xmm3, (%r8)
	vaddsd	%xmm6, %xmm5, %xmm3
	vsubsd	%xmm6, %xmm5, %xmm5
	vmovsd	%xmm7, (%rbx)
	vmovsd	%xmm3, (%r9)
	vaddsd	%xmm2, %xmm4, %xmm3
	vsubsd	%xmm2, %xmm4, %xmm4
	vmovsd	%xmm5, (%rdi)
	vmovsd	%xmm3, (%r10)
	vaddsd	%xmm1, %xmm0, %xmm3
	vsubsd	%xmm1, %xmm0, %xmm0
	vmovsd	%xmm4, (%rsi)
	vmovsd	%xmm3, (%r11)
	vmovsd	%xmm0, (%rdx)
.L23:
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%rbp
	.cfi_remember_state
	.cfi_def_cfa 7, 8
	ret
	.p2align 4,,10
	.p2align 3
.L29:
	.cfi_restore_state
	vzeroupper
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.p2align 4,,10
	.p2align 3
.L25:
	.cfi_restore 3
	.cfi_restore 6
	.cfi_restore 12
	.cfi_restore 13
	.cfi_restore 14
	ret
.L8:
	.cfi_def_cfa 6, 16
	.cfi_offset 3, -48
	.cfi_offset 6, -16
	.cfi_offset 12, -40
	.cfi_offset 13, -32
	.cfi_offset 14, -24
	xorl	%eax, %eax
	jmp	.L3
	.cfi_endproc
.LFE3:
	.size	t8, .-t8
	.p2align 4
	.globl	o8
	.type	o8, @function
o8:
.LFB4:
	.cfi_startproc
	endbr64
	testq	%rsi, %rsi
	je	.L54
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	leaq	-1(%rsi), %rax
	movq	%rdi, %rcx
	leaq	0(,%rsi,8), %rdx
	movq	%rsi, %rdi
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	.cfi_offset 14, -24
	.cfi_offset 13, -32
	.cfi_offset 12, -40
	.cfi_offset 3, -48
	cmpq	$2, %rax
	jbe	.L37
	leaq	(%rcx,%rdx), %rbx
	movq	%rdi, %r13
	xorl	%eax, %eax
	vbroadcastsd	.LC1(%rip), %ymm8
	leaq	(%rbx,%rdx), %r11
	shrq	$2, %r13
	leaq	(%r11,%rdx), %r10
	salq	$5, %r13
	leaq	(%r10,%rdx), %r9
	leaq	(%r9,%rdx), %r8
	leaq	(%r8,%rdx), %rsi
	leaq	(%rsi,%rdx), %r12
	.p2align 4,,10
	.p2align 3
.L33:
	vmovupd	(%rcx,%rax), %ymm3
	vmovupd	(%rbx,%rax), %ymm7
	vaddpd	(%r12,%rax), %ymm3, %ymm10
	vaddpd	(%rsi,%rax), %ymm7, %ymm6
	vmovupd	(%r11,%rax), %ymm3
	vmovupd	(%r10,%rax), %ymm7
	vsubpd	(%r8,%rax), %ymm3, %ymm1
	vsubpd	(%r9,%rax), %ymm7, %ymm5
	vsubpd	%ymm6, %ymm10, %ymm7
	vaddpd	%ymm5, %ymm1, %ymm9
	vsubpd	%ymm9, %ymm7, %ymm0
	vmulpd	%ymm8, %ymm0, %ymm0
	vsubpd	(%r12,%rax), %ymm0, %ymm4
	vsubpd	(%r8,%rax), %ymm0, %ymm0
	vaddpd	(%rsi,%rax), %ymm4, %ymm2
	vsubpd	(%r9,%rax), %ymm0, %ymm3
	vaddpd	(%rbx,%rax), %ymm4, %ymm4
	vaddpd	(%r10,%rax), %ymm0, %ymm0
	vsubpd	%ymm3, %ymm10, %ymm10
	vaddpd	%ymm2, %ymm1, %ymm1
	vaddpd	%ymm4, %ymm9, %ymm9
	vsubpd	%ymm0, %ymm7, %ymm7
	vmovupd	%ymm4, (%r11,%rax)
	vaddpd	%ymm3, %ymm6, %ymm6
	vaddpd	%ymm2, %ymm5, %ymm5
	vmovupd	%ymm0, (%r10,%rax)
	vmovupd	%ymm10, (%rcx,%rax)
	vmovupd	%ymm1, (%rbx,%rax)
	vmovupd	%ymm9, (%r9,%rax)
	vmovupd	%ymm7, (%r8,%rax)
	vmovupd	%ymm6, (%rsi,%rax)
	vmovupd	%ymm5, (%r12,%rax)
	addq	$32, %rax
	cmpq	%r13, %rax
	jne	.L33
	movq	%rdi, %rax
	andq	$-4, %rax
	testb	$3, %dil
	je	.L57
	vzeroupper
.L32:
	movq	%rdi, %r8
	subq	%rax, %r8
	cmpq	$1, %r8
	je	.L35
	leaq	(%rdi,%rax), %rsi
	leaq	(%rcx,%rax,8), %r10
	vmovddup	.LC1(%rip), %xmm13
	leaq	(%rcx,%rsi,8), %r9
	addq	%rdi, %rsi
	leaq	(%rcx,%rsi,8), %r11
	addq	%rdi, %rsi
	vmovupd	(%r9), %xmm3
	leaq	(%rcx,%rsi,8), %rbx
	addq	%rdi, %rsi
	vmovupd	(%r11), %xmm7
	leaq	(%rcx,%rsi,8), %r12
	addq	%rdi, %rsi
	vmovupd	(%rbx), %xmm2
	leaq	(%rcx,%rsi,8), %r13
	addq	%rdi, %rsi
	vmovupd	(%r12), %xmm6
	leaq	(%rcx,%rsi,8), %r14
	vmovupd	0(%r13), %xmm12
	addq	%rsi, %rdi
	vmovupd	(%r14), %xmm5
	leaq	(%rcx,%rdi,8), %rsi
	vsubpd	%xmm12, %xmm7, %xmm1
	vmovupd	(%rsi), %xmm4
	vsubpd	%xmm6, %xmm2, %xmm7
	vaddpd	(%r10), %xmm4, %xmm11
	vaddpd	%xmm5, %xmm3, %xmm8
	vaddpd	%xmm7, %xmm1, %xmm10
	vsubpd	%xmm8, %xmm11, %xmm9
	vsubpd	%xmm10, %xmm9, %xmm0
	vmulpd	%xmm13, %xmm0, %xmm0
	vsubpd	%xmm4, %xmm0, %xmm4
	vsubpd	%xmm12, %xmm0, %xmm0
	vaddpd	%xmm4, %xmm5, %xmm5
	vsubpd	%xmm6, %xmm0, %xmm6
	vaddpd	%xmm0, %xmm2, %xmm0
	vaddpd	%xmm4, %xmm3, %xmm2
	vaddpd	%xmm5, %xmm1, %xmm1
	vsubpd	%xmm6, %xmm11, %xmm11
	vaddpd	%xmm2, %xmm10, %xmm3
	vmovupd	%xmm2, (%r11)
	vsubpd	%xmm0, %xmm9, %xmm2
	vmovupd	%xmm0, (%rbx)
	vaddpd	%xmm5, %xmm7, %xmm0
	vmovupd	%xmm1, (%r9)
	vaddpd	%xmm6, %xmm8, %xmm1
	vmovupd	%xmm11, (%r10)
	vmovupd	%xmm3, (%r12)
	vmovupd	%xmm2, 0(%r13)
	vmovupd	%xmm1, (%r14)
	vmovupd	%xmm0, (%rsi)
	testb	$1, %r8b
	je	.L52
	andq	$-2, %r8
	addq	%r8, %rax
.L35:
	salq	$3, %rax
	leaq	(%rcx,%rax), %rsi
	addq	%rdx, %rax
	leaq	(%rcx,%rax), %rdi
	addq	%rdx, %rax
	leaq	(%rcx,%rax), %r8
	addq	%rdx, %rax
	vmovsd	(%rdi), %xmm3
	leaq	(%rcx,%rax), %r9
	addq	%rdx, %rax
	vmovsd	(%r8), %xmm1
	leaq	(%rcx,%rax), %r10
	addq	%rdx, %rax
	vmovsd	(%r9), %xmm2
	leaq	(%rcx,%rax), %r11
	addq	%rdx, %rax
	vmovsd	(%r10), %xmm9
	leaq	(%rcx,%rax), %rbx
	vmovsd	(%r11), %xmm12
	addq	%rax, %rdx
	vmovsd	(%rbx), %xmm6
	addq	%rcx, %rdx
	vsubsd	%xmm9, %xmm2, %xmm7
	vmovsd	(%rdx), %xmm4
	vsubsd	%xmm12, %xmm1, %xmm1
	vaddsd	(%rsi), %xmm4, %xmm11
	vaddsd	%xmm6, %xmm3, %xmm8
	vaddsd	%xmm7, %xmm1, %xmm10
	vsubsd	%xmm8, %xmm11, %xmm5
	vsubsd	%xmm10, %xmm5, %xmm0
	vmulsd	.LC1(%rip), %xmm0, %xmm0
	vsubsd	%xmm4, %xmm0, %xmm4
	vsubsd	%xmm12, %xmm0, %xmm0
	vaddsd	%xmm4, %xmm6, %xmm6
	vsubsd	%xmm9, %xmm0, %xmm9
	vaddsd	%xmm0, %xmm2, %xmm0
	vaddsd	%xmm4, %xmm3, %xmm2
	vaddsd	%xmm6, %xmm1, %xmm1
	vsubsd	%xmm9, %xmm11, %xmm11
	vsubsd	%xmm0, %xmm5, %xmm5
	vaddsd	%xmm9, %xmm8, %xmm8
	vmovsd	%xmm2, (%r8)
	vaddsd	%xmm6, %xmm7, %xmm6
	vaddsd	%xmm2, %xmm10, %xmm2
	vmovsd	%xmm0, (%r9)
	vmovsd	%xmm11, (%rsi)
	vmovsd	%xmm1, (%rdi)
	vmovsd	%xmm2, (%r10)
	vmovsd	%xmm5, (%r11)
	vmovsd	%xmm8, (%rbx)
	vmovsd	%xmm6, (%rdx)
.L52:
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%rbp
	.cfi_remember_state
	.cfi_def_cfa 7, 8
	ret
	.p2align 4,,10
	.p2align 3
.L57:
	.cfi_restore_state
	vzeroupper
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.p2align 4,,10
	.p2align 3
.L54:
	.cfi_restore 3
	.cfi_restore 6
	.cfi_restore 12
	.cfi_restore 13
	.cfi_restore 14
	ret
.L37:
	.cfi_def_cfa 6, 16
	.cfi_offset 3, -48
	.cfi_offset 6, -16
	.cfi_offset 12, -40
	.cfi_offset 13, -32
	.cfi_offset 14, -24
	xorl	%eax, %eax
	jmp	.L32
	.cfi_endproc
.LFE4:
	.size	o8, .-o8
	.p2align 4
	.globl	o8s
	.type	o8s, @function
o8s:
.LFB5:
	.cfi_startproc
	endbr64
	testq	%rsi, %rsi
	je	.L82
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	leaq	-1(%rsi), %rax
	movq	%rdi, %rcx
	vmovsd	%xmm0, %xmm0, %xmm1
	movq	%rsi, %rdi
	leaq	0(,%rsi,8), %rdx
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	.cfi_offset 14, -24
	.cfi_offset 13, -32
	.cfi_offset 12, -40
	.cfi_offset 3, -48
	cmpq	$2, %rax
	jbe	.L65
	leaq	(%rcx,%rdx), %rbx
	movq	%rdi, %r13
	vbroadcastsd	%xmm0, %ymm6
	xorl	%eax, %eax
	leaq	(%rbx,%rdx), %r11
	shrq	$2, %r13
	vbroadcastsd	.LC1(%rip), %ymm7
	leaq	(%r11,%rdx), %r10
	salq	$5, %r13
	leaq	(%r10,%rdx), %r9
	leaq	(%r9,%rdx), %r8
	leaq	(%r8,%rdx), %rsi
	leaq	(%rsi,%rdx), %r12
	.p2align 4,,10
	.p2align 3
.L61:
	vmovupd	(%rcx,%rax), %ymm4
	vmovupd	(%r11,%rax), %ymm3
	vaddpd	(%r12,%rax), %ymm4, %ymm5
	vsubpd	(%r8,%rax), %ymm3, %ymm0
	vmovupd	(%rbx,%rax), %ymm4
	vaddpd	(%rsi,%rax), %ymm4, %ymm9
	vmovupd	(%r10,%rax), %ymm4
	vsubpd	(%r9,%rax), %ymm4, %ymm8
	vsubpd	%ymm9, %ymm5, %ymm3
	vaddpd	%ymm8, %ymm0, %ymm4
	vsubpd	%ymm4, %ymm3, %ymm2
	vmulpd	%ymm7, %ymm2, %ymm2
	vsubpd	(%r12,%rax), %ymm2, %ymm13
	vsubpd	(%r8,%rax), %ymm2, %ymm2
	vaddpd	(%rsi,%rax), %ymm13, %ymm10
	vsubpd	(%r9,%rax), %ymm2, %ymm11
	vaddpd	(%rbx,%rax), %ymm13, %ymm13
	vaddpd	(%r10,%rax), %ymm2, %ymm12
	vsubpd	%ymm11, %ymm5, %ymm2
	vaddpd	%ymm10, %ymm0, %ymm5
	vmulpd	%ymm6, %ymm13, %ymm0
	vaddpd	%ymm13, %ymm4, %ymm4
	vsubpd	%ymm12, %ymm3, %ymm3
	vmulpd	%ymm6, %ymm2, %ymm2
	vmulpd	%ymm6, %ymm5, %ymm5
	vmulpd	%ymm6, %ymm4, %ymm4
	vmovupd	%ymm0, (%r11,%rax)
	vmulpd	%ymm6, %ymm12, %ymm0
	vmulpd	%ymm6, %ymm3, %ymm3
	vmovupd	%ymm2, (%rcx,%rax)
	vaddpd	%ymm11, %ymm9, %ymm2
	vmovupd	%ymm5, (%rbx,%rax)
	vmovupd	%ymm4, (%r9,%rax)
	vmovupd	%ymm0, (%r10,%rax)
	vaddpd	%ymm10, %ymm8, %ymm0
	vmulpd	%ymm6, %ymm2, %ymm2
	vmovupd	%ymm3, (%r8,%rax)
	vmulpd	%ymm6, %ymm0, %ymm0
	vmovupd	%ymm2, (%rsi,%rax)
	vmovupd	%ymm0, (%r12,%rax)
	addq	$32, %rax
	cmpq	%r13, %rax
	jne	.L61
	movq	%rdi, %rax
	andq	$-4, %rax
	testb	$3, %dil
	je	.L85
	vzeroupper
.L60:
	movq	%rdi, %r8
	subq	%rax, %r8
	cmpq	$1, %r8
	je	.L63
	leaq	(%rdi,%rax), %rsi
	leaq	(%rcx,%rax,8), %r10
	vmovddup	.LC1(%rip), %xmm15
	vmovddup	%xmm1, %xmm0
	leaq	(%rcx,%rsi,8), %r9
	addq	%rdi, %rsi
	leaq	(%rcx,%rsi,8), %r11
	addq	%rdi, %rsi
	vmovupd	(%r9), %xmm11
	leaq	(%rcx,%rsi,8), %rbx
	addq	%rdi, %rsi
	vmovupd	(%r11), %xmm7
	leaq	(%rcx,%rsi,8), %r12
	addq	%rdi, %rsi
	vmovupd	(%rbx), %xmm13
	leaq	(%rcx,%rsi,8), %r13
	addq	%rdi, %rsi
	vmovupd	(%r12), %xmm10
	leaq	(%rcx,%rsi,8), %r14
	vmovupd	0(%r13), %xmm14
	addq	%rsi, %rdi
	vmovupd	(%r14), %xmm9
	leaq	(%rcx,%rdi,8), %rsi
	vsubpd	%xmm14, %xmm7, %xmm2
	vmovupd	(%rsi), %xmm12
	vsubpd	%xmm10, %xmm13, %xmm7
	vaddpd	(%r10), %xmm12, %xmm6
	vaddpd	%xmm9, %xmm11, %xmm8
	vaddpd	%xmm7, %xmm2, %xmm5
	vsubpd	%xmm8, %xmm6, %xmm4
	vsubpd	%xmm5, %xmm4, %xmm3
	vmulpd	%xmm15, %xmm3, %xmm3
	vsubpd	%xmm12, %xmm3, %xmm12
	vsubpd	%xmm14, %xmm3, %xmm3
	vsubpd	%xmm10, %xmm3, %xmm10
	vaddpd	%xmm12, %xmm9, %xmm9
	vaddpd	%xmm12, %xmm11, %xmm11
	vaddpd	%xmm3, %xmm13, %xmm3
	vsubpd	%xmm10, %xmm6, %xmm6
	vsubpd	%xmm3, %xmm4, %xmm4
	vaddpd	%xmm11, %xmm5, %xmm5
	vmulpd	%xmm0, %xmm6, %xmm6
	vmulpd	%xmm0, %xmm5, %xmm5
	vmulpd	%xmm0, %xmm4, %xmm4
	vmovupd	%xmm6, (%r10)
	vaddpd	%xmm9, %xmm2, %xmm6
	vmulpd	%xmm0, %xmm11, %xmm2
	vmovupd	%xmm5, (%r12)
	vmovupd	%xmm4, 0(%r13)
	vmulpd	%xmm0, %xmm6, %xmm6
	vmovupd	%xmm2, (%r11)
	vmulpd	%xmm0, %xmm3, %xmm2
	vaddpd	%xmm10, %xmm8, %xmm3
	vmulpd	%xmm0, %xmm3, %xmm3
	vmovupd	%xmm6, (%r9)
	vmovupd	%xmm2, (%rbx)
	vaddpd	%xmm9, %xmm7, %xmm2
	vmulpd	%xmm0, %xmm2, %xmm0
	vmovupd	%xmm3, (%r14)
	vmovupd	%xmm0, (%rsi)
	testb	$1, %r8b
	je	.L80
	andq	$-2, %r8
	addq	%r8, %rax
.L63:
	salq	$3, %rax
	leaq	(%rcx,%rax), %rsi
	addq	%rdx, %rax
	leaq	(%rcx,%rax), %rdi
	addq	%rdx, %rax
	leaq	(%rcx,%rax), %r8
	addq	%rdx, %rax
	vmovsd	(%rdi), %xmm12
	leaq	(%rcx,%rax), %r9
	addq	%rdx, %rax
	vmovsd	(%r8), %xmm5
	leaq	(%rcx,%rax), %r10
	addq	%rdx, %rax
	vmovsd	(%r9), %xmm11
	leaq	(%rcx,%rax), %r11
	addq	%rdx, %rax
	vmovsd	(%r10), %xmm9
	leaq	(%rcx,%rax), %rbx
	vmovsd	(%r11), %xmm13
	addq	%rax, %rdx
	vmovsd	(%rbx), %xmm8
	addq	%rcx, %rdx
	vsubsd	%xmm9, %xmm11, %xmm6
	vmovsd	(%rdx), %xmm10
	vsubsd	%xmm13, %xmm5, %xmm5
	vaddsd	(%rsi), %xmm10, %xmm7
	vaddsd	%xmm8, %xmm12, %xmm2
	vaddsd	%xmm6, %xmm5, %xmm4
	vsubsd	%xmm2, %xmm7, %xmm3
	vsubsd	%xmm4, %xmm3, %xmm0
	vmulsd	.LC1(%rip), %xmm0, %xmm0
	vsubsd	%xmm10, %xmm0, %xmm10
	vsubsd	%xmm13, %xmm0, %xmm0
	vaddsd	%xmm10, %xmm8, %xmm8
	vsubsd	%xmm9, %xmm0, %xmm9
	vaddsd	%xmm0, %xmm11, %xmm11
	vaddsd	%xmm10, %xmm12, %xmm0
	vaddsd	%xmm8, %xmm5, %xmm5
	vsubsd	%xmm9, %xmm7, %xmm7
	vaddsd	%xmm0, %xmm4, %xmm4
	vsubsd	%xmm11, %xmm3, %xmm3
	vaddsd	%xmm9, %xmm2, %xmm2
	vmulsd	%xmm1, %xmm5, %xmm5
	vmulsd	%xmm1, %xmm7, %xmm7
	vmulsd	%xmm1, %xmm4, %xmm4
	vmulsd	%xmm1, %xmm3, %xmm3
	vmulsd	%xmm1, %xmm2, %xmm2
	vmovsd	%xmm5, (%rdi)
	vmulsd	%xmm0, %xmm1, %xmm5
	vaddsd	%xmm8, %xmm6, %xmm0
	vmovsd	%xmm7, (%rsi)
	vmovsd	%xmm4, (%r10)
	vmulsd	%xmm1, %xmm0, %xmm0
	vmovsd	%xmm3, (%r11)
	vmovsd	%xmm2, (%rbx)
	vmovsd	%xmm5, (%r8)
	vmulsd	%xmm11, %xmm1, %xmm5
	vmovsd	%xmm0, (%rdx)
	vmovsd	%xmm5, (%r9)
.L80:
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%rbp
	.cfi_remember_state
	.cfi_def_cfa 7, 8
	ret
	.p2align 4,,10
	.p2align 3
.L85:
	.cfi_restore_state
	vzeroupper
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.p2align 4,,10
	.p2align 3
.L82:
	.cfi_restore 3
	.cfi_restore 6
	.cfi_restore 12
	.cfi_restore 13
	.cfi_restore 14
	ret
.L65:
	.cfi_def_cfa 6, 16
	.cfi_offset 3, -48
	.cfi_offset 6, -16
	.cfi_offset 12, -40
	.cfi_offset 13, -32
	.cfi_offset 14, -24
	xorl	%eax, %eax
	jmp	.L60
	.cfi_endproc
.LFE5:
	.size	o8s, .-o8s
	.section	.rodata.cst8,"aM",@progbits,8
	.align 8
.LC1:
	.long	0
	.long	1071644672
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:

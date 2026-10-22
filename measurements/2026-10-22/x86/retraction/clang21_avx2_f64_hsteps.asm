000000000003b4d0 <hfirst_kid_nat>:
   3b4d0:      	vmovaps	(%rip), %ymm0           # 0x3b4d8 <hfirst_kid_nat+0x8>
   3b4d8:      	testq	%rsi, %rsi
   3b4db:      	je	0x3b528 <hfirst_kid_nat+0x58>
   3b4dd:      	xorl	%eax, %eax
   3b4df:      	vxorpd	%xmm0, %xmm0, %xmm0
   3b4e3:      	nopw	%cs:(%rax,%rax)
   3b4f0:      	vmovupd	(%rdi,%rax,8), %ymm1
   3b4f5:      	vmovddup	%ymm1, %ymm2            # ymm2 = ymm1[0,0,2,2]
   3b4f9:      	vshufpd	$0xf, %ymm1, %ymm1, %ymm1 # ymm1 = ymm1[1,1,3,3]
   3b4fe:      	vsubpd	%ymm1, %ymm0, %ymm1
   3b502:      	vaddsubpd	%ymm1, %ymm2, %ymm1
   3b506:      	vpermpd	$0x44, %ymm1, %ymm2     # ymm2 = ymm1[0,1,0,1]
   3b50c:      	vsubpd	%ymm1, %ymm0, %ymm3
   3b510:      	vperm2f128	$0x31, %ymm3, %ymm1, %ymm1 # ymm1 = ymm1[2,3],ymm3[2,3]
   3b516:      	vaddpd	%ymm1, %ymm2, %ymm1
   3b51a:      	vmovupd	%ymm1, (%rdi,%rax,8)
   3b51f:      	addq	$0x4, %rax
   3b523:      	cmpq	%rsi, %rax
   3b526:      	jb	0x3b4f0 <hfirst_kid_nat+0x20>
   3b528:      	vzeroupper
   3b52b:      	retq
   3b52c:      	nopl	(%rax)

000000000003b530 <hfirst_tb2_nat>:
   3b530:      	vmovaps	(%rip), %ymm0           # 0x3b538 <hfirst_tb2_nat+0x8>
   3b538:      	testq	%rsi, %rsi
   3b53b:      	je	0x3b5c1 <hfirst_tb2_nat+0x91>
   3b541:      	xorl	%eax, %eax
   3b543:      	vxorpd	%xmm0, %xmm0, %xmm0
   3b547:      	nopw	(%rax,%rax)
   3b550:      	vmovupd	(%rdi,%rax,8), %ymm1
   3b555:      	vmovupd	0x20(%rdi,%rax,8), %ymm2
   3b55b:      	vmovddup	%ymm1, %ymm3            # ymm3 = ymm1[0,0,2,2]
   3b55f:      	vshufpd	$0xf, %ymm1, %ymm1, %ymm1 # ymm1 = ymm1[1,1,3,3]
   3b564:      	vsubpd	%ymm1, %ymm0, %ymm1
   3b568:      	vaddsubpd	%ymm1, %ymm3, %ymm1
   3b56c:      	vpermpd	$0x44, %ymm1, %ymm3     # ymm3 = ymm1[0,1,0,1]
   3b572:      	vsubpd	%ymm1, %ymm0, %ymm4
   3b576:      	vperm2f128	$0x31, %ymm4, %ymm1, %ymm1 # ymm1 = ymm1[2,3],ymm4[2,3]
   3b57c:      	vaddpd	%ymm1, %ymm3, %ymm1
   3b580:      	vmovddup	%ymm2, %ymm3            # ymm3 = ymm2[0,0,2,2]
   3b584:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3b589:      	vsubpd	%ymm2, %ymm0, %ymm2
   3b58d:      	vaddsubpd	%ymm2, %ymm3, %ymm2
   3b591:      	vpermpd	$0x44, %ymm2, %ymm3     # ymm3 = ymm2[0,1,0,1]
   3b597:      	vsubpd	%ymm2, %ymm0, %ymm4
   3b59b:      	vperm2f128	$0x31, %ymm4, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm4[2,3]
   3b5a1:      	vaddpd	%ymm2, %ymm3, %ymm2
   3b5a5:      	vaddpd	%ymm2, %ymm1, %ymm3
   3b5a9:      	vsubpd	%ymm2, %ymm1, %ymm1
   3b5ad:      	vmovupd	%ymm3, (%rdi,%rax,8)
   3b5b2:      	vmovupd	%ymm1, 0x20(%rdi,%rax,8)
   3b5b8:      	addq	$0x8, %rax
   3b5bc:      	cmpq	%rsi, %rax
   3b5bf:      	jb	0x3b550 <hfirst_tb2_nat+0x20>
   3b5c1:      	vzeroupper
   3b5c4:      	retq
   3b5c5:      	nopw	%cs:(%rax,%rax)

000000000003b5d0 <hfirst_tb4_nat>:
   3b5d0:      	vmovaps	(%rip), %ymm0           # 0x3b5d8 <hfirst_tb4_nat+0x8>
   3b5d8:      	testq	%rsi, %rsi
   3b5db:      	je	0x3b6df <hfirst_tb4_nat+0x10f>
   3b5e1:      	xorl	%eax, %eax
   3b5e3:      	vxorpd	%xmm0, %xmm0, %xmm0
   3b5e7:      	nopw	(%rax,%rax)
   3b5f0:      	vmovupd	(%rdi,%rax,8), %ymm1
   3b5f5:      	vmovupd	0x20(%rdi,%rax,8), %ymm2
   3b5fb:      	vmovupd	0x40(%rdi,%rax,8), %ymm3
   3b601:      	vmovupd	0x60(%rdi,%rax,8), %ymm4
   3b607:      	vmovddup	%ymm1, %ymm5            # ymm5 = ymm1[0,0,2,2]
   3b60b:      	vshufpd	$0xf, %ymm1, %ymm1, %ymm1 # ymm1 = ymm1[1,1,3,3]
   3b610:      	vsubpd	%ymm1, %ymm0, %ymm1
   3b614:      	vaddsubpd	%ymm1, %ymm5, %ymm1
   3b618:      	vpermpd	$0x44, %ymm1, %ymm5     # ymm5 = ymm1[0,1,0,1]
   3b61e:      	vsubpd	%ymm1, %ymm0, %ymm6
   3b622:      	vperm2f128	$0x31, %ymm6, %ymm1, %ymm1 # ymm1 = ymm1[2,3],ymm6[2,3]
   3b628:      	vaddpd	%ymm1, %ymm5, %ymm1
   3b62c:      	vmovddup	%ymm2, %ymm5            # ymm5 = ymm2[0,0,2,2]
   3b630:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3b635:      	vsubpd	%ymm2, %ymm0, %ymm2
   3b639:      	vaddsubpd	%ymm2, %ymm5, %ymm2
   3b63d:      	vpermpd	$0x44, %ymm2, %ymm5     # ymm5 = ymm2[0,1,0,1]
   3b643:      	vsubpd	%ymm2, %ymm0, %ymm6
   3b647:      	vperm2f128	$0x31, %ymm6, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm6[2,3]
   3b64d:      	vaddpd	%ymm2, %ymm5, %ymm2
   3b651:      	vmovddup	%ymm3, %ymm5            # ymm5 = ymm3[0,0,2,2]
   3b655:      	vshufpd	$0xf, %ymm3, %ymm3, %ymm3 # ymm3 = ymm3[1,1,3,3]
   3b65a:      	vsubpd	%ymm3, %ymm0, %ymm3
   3b65e:      	vaddsubpd	%ymm3, %ymm5, %ymm3
   3b662:      	vpermpd	$0x44, %ymm3, %ymm5     # ymm5 = ymm3[0,1,0,1]
   3b668:      	vsubpd	%ymm3, %ymm0, %ymm6
   3b66c:      	vperm2f128	$0x31, %ymm6, %ymm3, %ymm3 # ymm3 = ymm3[2,3],ymm6[2,3]
   3b672:      	vaddpd	%ymm3, %ymm5, %ymm3
   3b676:      	vmovddup	%ymm4, %ymm5            # ymm5 = ymm4[0,0,2,2]
   3b67a:      	vshufpd	$0xf, %ymm4, %ymm4, %ymm4 # ymm4 = ymm4[1,1,3,3]
   3b67f:      	vsubpd	%ymm4, %ymm0, %ymm4
   3b683:      	vaddsubpd	%ymm4, %ymm5, %ymm4
   3b687:      	vpermpd	$0x44, %ymm4, %ymm5     # ymm5 = ymm4[0,1,0,1]
   3b68d:      	vsubpd	%ymm4, %ymm0, %ymm6
   3b691:      	vperm2f128	$0x31, %ymm6, %ymm4, %ymm4 # ymm4 = ymm4[2,3],ymm6[2,3]
   3b697:      	vaddpd	%ymm4, %ymm5, %ymm4
   3b69b:      	vaddpd	%ymm2, %ymm1, %ymm5
   3b69f:      	vsubpd	%ymm2, %ymm1, %ymm1
   3b6a3:      	vaddpd	%ymm4, %ymm3, %ymm2
   3b6a7:      	vsubpd	%ymm4, %ymm3, %ymm3
   3b6ab:      	vaddpd	%ymm2, %ymm5, %ymm4
   3b6af:      	vsubpd	%ymm2, %ymm5, %ymm2
   3b6b3:      	vaddpd	%ymm3, %ymm1, %ymm5
   3b6b7:      	vsubpd	%ymm3, %ymm1, %ymm1
   3b6bb:      	vmovupd	%ymm4, (%rdi,%rax,8)
   3b6c0:      	vmovupd	%ymm5, 0x20(%rdi,%rax,8)
   3b6c6:      	vmovupd	%ymm2, 0x40(%rdi,%rax,8)
   3b6cc:      	vmovupd	%ymm1, 0x60(%rdi,%rax,8)
   3b6d2:      	addq	$0x10, %rax
   3b6d6:      	cmpq	%rsi, %rax
   3b6d9:      	jb	0x3b5f0 <hfirst_tb4_nat+0x20>
   3b6df:      	vzeroupper
   3b6e2:      	retq
   3b6e3:      	nopw	%cs:(%rax,%rax)

000000000003b6f0 <hfirst_broken_g20>:
   3b6f0:      	vmovaps	(%rip), %ymm0           # 0x3b6f8 <hfirst_broken_g20+0x8>
   3b6f8:      	testq	%rsi, %rsi
   3b6fb:      	je	0x3b91f <hfirst_broken_g20+0x22f>
   3b701:      	xorl	%eax, %eax
   3b703:      	vxorpd	%xmm0, %xmm0, %xmm0
   3b707:      	vbroadcastsd	(%rip), %ymm1   # 0x3b710 <hfirst_broken_g20+0x20>
   3b710:      	vmovupd	(%rdi,%rax,8), %ymm2
   3b715:      	vmovupd	0x20(%rdi,%rax,8), %ymm3
   3b71b:      	vmovupd	0x40(%rdi,%rax,8), %ymm4
   3b721:      	vmovupd	0x60(%rdi,%rax,8), %ymm6
   3b727:      	vmovddup	%ymm2, %ymm5            # ymm5 = ymm2[0,0,2,2]
   3b72b:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3b730:      	vsubpd	%ymm2, %ymm0, %ymm2
   3b734:      	vaddsubpd	%ymm2, %ymm5, %ymm2
   3b738:      	vpermpd	$0x44, %ymm2, %ymm5     # ymm5 = ymm2[0,1,0,1]
   3b73e:      	vsubpd	%ymm2, %ymm0, %ymm7
   3b742:      	vperm2f128	$0x31, %ymm7, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm7[2,3]
   3b748:      	vaddpd	%ymm2, %ymm5, %ymm2
   3b74c:      	vmovddup	%ymm3, %ymm5            # ymm5 = ymm3[0,0,2,2]
   3b750:      	vshufpd	$0xf, %ymm3, %ymm3, %ymm3 # ymm3 = ymm3[1,1,3,3]
   3b755:      	vsubpd	%ymm3, %ymm0, %ymm3
   3b759:      	vaddsubpd	%ymm3, %ymm5, %ymm3
   3b75d:      	vpermpd	$0x44, %ymm3, %ymm5     # ymm5 = ymm3[0,1,0,1]
   3b763:      	vsubpd	%ymm3, %ymm0, %ymm7
   3b767:      	vperm2f128	$0x31, %ymm7, %ymm3, %ymm3 # ymm3 = ymm3[2,3],ymm7[2,3]
   3b76d:      	vaddpd	%ymm3, %ymm5, %ymm5
   3b771:      	vmovddup	%ymm4, %ymm3            # ymm3 = ymm4[0,0,2,2]
   3b775:      	vshufpd	$0xf, %ymm4, %ymm4, %ymm4 # ymm4 = ymm4[1,1,3,3]
   3b77a:      	vsubpd	%ymm4, %ymm0, %ymm4
   3b77e:      	vaddsubpd	%ymm4, %ymm3, %ymm3
   3b782:      	vpermpd	$0x44, %ymm3, %ymm4     # ymm4 = ymm3[0,1,0,1]
   3b788:      	vsubpd	%ymm3, %ymm0, %ymm7
   3b78c:      	vperm2f128	$0x31, %ymm7, %ymm3, %ymm3 # ymm3 = ymm3[2,3],ymm7[2,3]
   3b792:      	vaddpd	%ymm3, %ymm4, %ymm3
   3b796:      	vmovddup	%ymm6, %ymm4            # ymm4 = ymm6[0,0,2,2]
   3b79a:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm6 # ymm6 = ymm6[1,1,3,3]
   3b79f:      	vsubpd	%ymm6, %ymm0, %ymm6
   3b7a3:      	vaddsubpd	%ymm6, %ymm4, %ymm4
   3b7a7:      	vpermpd	$0x44, %ymm4, %ymm6     # ymm6 = ymm4[0,1,0,1]
   3b7ad:      	vsubpd	%ymm4, %ymm0, %ymm7
   3b7b1:      	vperm2f128	$0x31, %ymm7, %ymm4, %ymm4 # ymm4 = ymm4[2,3],ymm7[2,3]
   3b7b7:      	vaddpd	%ymm4, %ymm6, %ymm7
   3b7bb:      	vmovupd	0x80(%rdi,%rax,8), %ymm4
   3b7c4:      	vmovddup	%ymm4, %ymm6            # ymm6 = ymm4[0,0,2,2]
   3b7c8:      	vshufpd	$0xf, %ymm4, %ymm4, %ymm4 # ymm4 = ymm4[1,1,3,3]
   3b7cd:      	vsubpd	%ymm4, %ymm0, %ymm4
   3b7d1:      	vaddsubpd	%ymm4, %ymm6, %ymm4
   3b7d5:      	vpermpd	$0x44, %ymm4, %ymm6     # ymm6 = ymm4[0,1,0,1]
   3b7db:      	vsubpd	%ymm4, %ymm0, %ymm8
   3b7df:      	vperm2f128	$0x31, %ymm8, %ymm4, %ymm4 # ymm4 = ymm4[2,3],ymm8[2,3]
   3b7e5:      	vaddpd	%ymm4, %ymm6, %ymm4
   3b7e9:      	vmovupd	0xa0(%rdi,%rax,8), %ymm6
   3b7f2:      	vmovddup	%ymm6, %ymm8            # ymm8 = ymm6[0,0,2,2]
   3b7f6:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm6 # ymm6 = ymm6[1,1,3,3]
   3b7fb:      	vsubpd	%ymm6, %ymm0, %ymm6
   3b7ff:      	vaddsubpd	%ymm6, %ymm8, %ymm6
   3b803:      	vpermpd	$0x44, %ymm6, %ymm8     # ymm8 = ymm6[0,1,0,1]
   3b809:      	vsubpd	%ymm6, %ymm0, %ymm9
   3b80d:      	vperm2f128	$0x31, %ymm9, %ymm6, %ymm6 # ymm6 = ymm6[2,3],ymm9[2,3]
   3b813:      	vaddpd	%ymm6, %ymm8, %ymm8
   3b817:      	vmovupd	0xc0(%rdi,%rax,8), %ymm6
   3b820:      	vmovddup	%ymm6, %ymm9            # ymm9 = ymm6[0,0,2,2]
   3b824:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm6 # ymm6 = ymm6[1,1,3,3]
   3b829:      	vsubpd	%ymm6, %ymm0, %ymm6
   3b82d:      	vaddsubpd	%ymm6, %ymm9, %ymm6
   3b831:      	vpermpd	$0x44, %ymm6, %ymm9     # ymm9 = ymm6[0,1,0,1]
   3b837:      	vsubpd	%ymm6, %ymm0, %ymm10
   3b83b:      	vperm2f128	$0x31, %ymm10, %ymm6, %ymm6 # ymm6 = ymm6[2,3],ymm10[2,3]
   3b841:      	vaddpd	%ymm6, %ymm9, %ymm6
   3b845:      	vmovupd	0xe0(%rdi,%rax,8), %ymm9
   3b84e:      	vmovddup	%ymm9, %ymm10           # ymm10 = ymm9[0,0,2,2]
   3b853:      	vshufpd	$0xf, %ymm9, %ymm9, %ymm9 # ymm9 = ymm9[1,1,3,3]
   3b859:      	vsubpd	%ymm9, %ymm0, %ymm9
   3b85e:      	vaddsubpd	%ymm9, %ymm10, %ymm9
   3b863:      	vpermpd	$0x44, %ymm9, %ymm10    # ymm10 = ymm9[0,1,0,1]
   3b869:      	vsubpd	%ymm9, %ymm0, %ymm11
   3b86e:      	vperm2f128	$0x31, %ymm11, %ymm9, %ymm9 # ymm9 = ymm9[2,3],ymm11[2,3]
   3b874:      	vaddpd	%ymm9, %ymm10, %ymm9
   3b879:      	vaddpd	%ymm5, %ymm2, %ymm5
   3b87d:      	vsubpd	%ymm7, %ymm3, %ymm7
   3b881:      	vsubpd	%ymm7, %ymm5, %ymm10
   3b885:      	vfmadd213pd	%ymm10, %ymm1, %ymm3 # ymm3 = (ymm1 * ymm3) + ymm10
   3b88a:      	vfmsub213pd	%ymm10, %ymm1, %ymm2 # ymm2 = (ymm1 * ymm2) - ymm10
   3b88f:      	vaddpd	%ymm4, %ymm8, %ymm8
   3b893:      	vsubpd	%ymm9, %ymm6, %ymm9
   3b898:      	vaddpd	%ymm9, %ymm8, %ymm10
   3b89d:      	vfnmadd213pd	%ymm10, %ymm1, %ymm6 # ymm6 = -(ymm1 * ymm6) + ymm10
   3b8a2:      	vfmsub213pd	%ymm10, %ymm1, %ymm4 # ymm4 = (ymm1 * ymm4) - ymm10
   3b8a7:      	vaddpd	%ymm6, %ymm3, %ymm10
   3b8ab:      	vfnmadd213pd	%ymm10, %ymm1, %ymm8 # ymm8 = -(ymm1 * ymm8) + ymm10
   3b8b0:      	vfmsub213pd	%ymm10, %ymm1, %ymm5 # ymm5 = (ymm1 * ymm5) - ymm10
   3b8b5:      	vfmsub213pd	%ymm8, %ymm1, %ymm3 # ymm3 = (ymm1 * ymm3) - ymm8
   3b8ba:      	vfmadd213pd	%ymm5, %ymm1, %ymm6 # ymm6 = (ymm1 * ymm6) + ymm5
   3b8bf:      	vaddpd	%ymm4, %ymm2, %ymm10
   3b8c3:      	vfmadd213pd	%ymm10, %ymm1, %ymm9 # ymm9 = (ymm1 * ymm9) + ymm10
   3b8c8:      	vfnmadd213pd	%ymm10, %ymm1, %ymm7 # ymm7 = -(ymm1 * ymm7) + ymm10
   3b8cd:      	vfmsub213pd	%ymm9, %ymm1, %ymm2 # ymm2 = (ymm1 * ymm2) - ymm9
   3b8d2:      	vfnmadd213pd	%ymm7, %ymm1, %ymm4 # ymm4 = -(ymm1 * ymm4) + ymm7
   3b8d7:      	vmovupd	%ymm3, (%rdi,%rax,8)
   3b8dc:      	vmovupd	%ymm9, 0x20(%rdi,%rax,8)
   3b8e2:      	vmovupd	%ymm6, 0x40(%rdi,%rax,8)
   3b8e8:      	vmovupd	%ymm7, 0x60(%rdi,%rax,8)
   3b8ee:      	vmovupd	%ymm8, 0x80(%rdi,%rax,8)
   3b8f7:      	vmovupd	%ymm5, 0xa0(%rdi,%rax,8)
   3b900:      	vmovupd	%ymm2, 0xc0(%rdi,%rax,8)
   3b909:      	vmovupd	%ymm4, 0xe0(%rdi,%rax,8)
   3b912:      	addq	$0x20, %rax
   3b916:      	cmpq	%rsi, %rax
   3b919:      	jb	0x3b710 <hfirst_broken_g20+0x20>
   3b91f:      	vzeroupper
   3b922:      	retq
   3b923:      	nopw	%cs:(%rax,%rax)

000000000003b930 <hstep_tb2_nat>:
   3b930:      	pushq	%r15
   3b932:      	pushq	%r14
   3b934:      	pushq	%r12
   3b936:      	pushq	%rbx
   3b937:      	vmovaps	(%rip), %ymm0           # 0x3b93f <hstep_tb2_nat+0xf>
   3b93f:      	testq	%rsi, %rsi
   3b942:      	je	0x3ba34 <hstep_tb2_nat+0x104>
   3b948:      	testq	%rdx, %rdx
   3b94b:      	je	0x3ba34 <hstep_tb2_nat+0x104>
   3b951:      	leaq	(%rdx,%rdx), %rax
   3b955:      	leaq	-0x1(%rdx), %rcx
   3b959:      	movq	%rcx, %r8
   3b95c:      	shrq	$0x2, %r8
   3b960:      	incq	%r8
   3b963:      	andq	$-0x2, %r8
   3b967:      	leaq	0x20(%rdi), %r9
   3b96b:      	movq	%rdx, %r10
   3b96e:      	shlq	$0x4, %r10
   3b972:      	leaq	(,%rdx,8), %r11
   3b97a:      	xorl	%ebx, %ebx
   3b97c:      	jmp	0x3b98f <hstep_tb2_nat+0x5f>
   3b97e:      	nop
   3b980:      	addq	%rax, %rbx
   3b983:      	addq	%r10, %r9
   3b986:      	cmpq	%rsi, %rbx
   3b989:      	jae	0x3ba34 <hstep_tb2_nat+0x104>
   3b98f:      	cmpq	$0x5, %rdx
   3b993:      	jae	0x3b9a0 <hstep_tb2_nat+0x70>
   3b995:      	xorl	%r14d, %r14d
   3b998:      	jmp	0x3b9fe <hstep_tb2_nat+0xce>
   3b99a:      	nopw	(%rax,%rax)
   3b9a0:      	leaq	(%r9,%r11), %r15
   3b9a4:      	movq	%r8, %r12
   3b9a7:      	xorl	%r14d, %r14d
   3b9aa:      	nopw	(%rax,%rax)
   3b9b0:      	vmovupd	-0x20(%r9,%r14,8), %ymm0
   3b9b7:      	vmovupd	-0x20(%r15,%r14,8), %ymm1
   3b9be:      	vaddpd	%ymm1, %ymm0, %ymm2
   3b9c2:      	vsubpd	%ymm1, %ymm0, %ymm0
   3b9c6:      	vmovupd	%ymm2, -0x20(%r9,%r14,8)
   3b9cd:      	vmovupd	%ymm0, -0x20(%r15,%r14,8)
   3b9d4:      	vmovupd	(%r9,%r14,8), %ymm0
   3b9da:      	vmovupd	(%r15,%r14,8), %ymm1
   3b9e0:      	vaddpd	%ymm1, %ymm0, %ymm2
   3b9e4:      	vsubpd	%ymm1, %ymm0, %ymm0
   3b9e8:      	vmovupd	%ymm2, (%r9,%r14,8)
   3b9ee:      	vmovupd	%ymm0, (%r15,%r14,8)
   3b9f4:      	addq	$0x8, %r14
   3b9f8:      	addq	$-0x2, %r12
   3b9fc:      	jne	0x3b9b0 <hstep_tb2_nat+0x80>
   3b9fe:      	testb	$0x4, %cl
   3ba01:      	jne	0x3b980 <hstep_tb2_nat+0x50>
   3ba07:      	leaq	(%rdi,%rbx,8), %r15
   3ba0b:      	leaq	(%r15,%r14,8), %r12
   3ba0f:      	vmovupd	(%r15,%r14,8), %ymm0
   3ba15:      	vmovupd	(%r12,%rdx,8), %ymm1
   3ba1b:      	vaddpd	%ymm1, %ymm0, %ymm2
   3ba1f:      	vsubpd	%ymm1, %ymm0, %ymm0
   3ba23:      	vmovupd	%ymm2, (%r15,%r14,8)
   3ba29:      	vmovupd	%ymm0, (%r12,%rdx,8)
   3ba2f:      	jmp	0x3b980 <hstep_tb2_nat+0x50>
   3ba34:      	popq	%rbx
   3ba35:      	popq	%r12
   3ba37:      	popq	%r14
   3ba39:      	popq	%r15
   3ba3b:      	vzeroupper
   3ba3e:      	retq
   3ba3f:      	nop

000000000003ba40 <hstep_tb4_nat>:
   3ba40:      	pushq	%rbx
   3ba41:      	vmovaps	(%rip), %ymm0           # 0x3ba49 <hstep_tb4_nat+0x9>
   3ba49:      	testq	%rsi, %rsi
   3ba4c:      	je	0x3baf1 <hstep_tb4_nat+0xb1>
   3ba52:      	testq	%rdx, %rdx
   3ba55:      	je	0x3baf1 <hstep_tb4_nat+0xb1>
   3ba5b:      	leaq	(,%rdx,4), %rax
   3ba63:      	movq	%rdx, %rcx
   3ba66:      	shlq	$0x4, %rcx
   3ba6a:      	leaq	(,%rdx,8), %r8
   3ba72:      	leaq	(%r8,%r8,2), %r8
   3ba76:      	xorl	%r9d, %r9d
   3ba79:      	nopl	(%rax)
   3ba80:      	leaq	(%rdi,%r9,8), %r10
   3ba84:      	xorl	%r11d, %r11d
   3ba87:      	nopw	(%rax,%rax)
   3ba90:      	leaq	(%r10,%r11,8), %rbx
   3ba94:      	vmovupd	(%r10,%r11,8), %ymm0
   3ba9a:      	vmovupd	(%rbx,%rdx,8), %ymm1
   3ba9f:      	vmovupd	(%rcx,%rbx), %ymm2
   3baa4:      	vmovupd	(%r8,%rbx), %ymm3
   3baaa:      	vaddpd	%ymm1, %ymm0, %ymm4
   3baae:      	vsubpd	%ymm1, %ymm0, %ymm0
   3bab2:      	vaddpd	%ymm3, %ymm2, %ymm1
   3bab6:      	vsubpd	%ymm3, %ymm2, %ymm2
   3baba:      	vaddpd	%ymm1, %ymm4, %ymm3
   3babe:      	vsubpd	%ymm1, %ymm4, %ymm1
   3bac2:      	vaddpd	%ymm2, %ymm0, %ymm4
   3bac6:      	vsubpd	%ymm2, %ymm0, %ymm0
   3baca:      	vmovupd	%ymm3, (%r10,%r11,8)
   3bad0:      	vmovupd	%ymm4, (%rbx,%rdx,8)
   3bad5:      	vmovupd	%ymm1, (%rcx,%rbx)
   3bada:      	vmovupd	%ymm0, (%r8,%rbx)
   3bae0:      	addq	$0x4, %r11
   3bae4:      	cmpq	%rdx, %r11
   3bae7:      	jb	0x3ba90 <hstep_tb4_nat+0x50>
   3bae9:      	addq	%rax, %r9
   3baec:      	cmpq	%rsi, %r9
   3baef:      	jb	0x3ba80 <hstep_tb4_nat+0x40>
   3baf1:      	popq	%rbx
   3baf2:      	vzeroupper
   3baf5:      	retq
   3baf6:      	nopw	%cs:(%rax,%rax)

000000000003bb00 <hstep_broken_g20>:
   3bb00:      	pushq	%r15
   3bb02:      	pushq	%r14
   3bb04:      	pushq	%r13
   3bb06:      	pushq	%r12
   3bb08:      	pushq	%rbx
   3bb09:      	vmovaps	(%rip), %ymm0           # 0x3bb11 <hstep_broken_g20+0x11>
   3bb11:      	testq	%rsi, %rsi
   3bb14:      	je	0x3bc6e <hstep_broken_g20+0x16e>
   3bb1a:      	testq	%rdx, %rdx
   3bb1d:      	je	0x3bc6e <hstep_broken_g20+0x16e>
   3bb23:      	leaq	(,%rdx,8), %rax
   3bb2b:      	movq	%rdx, %rcx
   3bb2e:      	shlq	$0x4, %rcx
   3bb32:      	leaq	(%rdx,%rdx,2), %r8
   3bb36:      	movq	%rdx, %r9
   3bb39:      	shlq	$0x5, %r9
   3bb3d:      	leaq	(%rdx,%rdx,4), %r14
   3bb41:      	leaq	(%rdi,%r8,8), %r10
   3bb45:      	shlq	$0x4, %r8
   3bb49:      	imulq	$0x38, %rdx, %r11
   3bb4d:      	addq	%rdi, %r11
   3bb50:      	movq	%rdx, %rbx
   3bb53:      	shlq	$0x6, %rbx
   3bb57:      	addq	%rdi, %r8
   3bb5a:      	leaq	(%rdi,%r14,8), %r14
   3bb5e:      	addq	%rdi, %r9
   3bb61:      	addq	%rdi, %rcx
   3bb64:      	leaq	(%rdi,%rax), %r15
   3bb68:      	xorl	%r12d, %r12d
   3bb6b:      	vbroadcastsd	(%rip), %ymm0   # 0x3bb74 <hstep_broken_g20+0x74>
   3bb74:      	nopw	%cs:(%rax,%rax)
   3bb80:      	xorl	%r13d, %r13d
   3bb83:      	nopw	%cs:(%rax,%rax)
   3bb90:      	vmovupd	(%rdi,%r13,8), %ymm1
   3bb96:      	vmovupd	(%rcx,%r13,8), %ymm4
   3bb9c:      	vmovupd	(%r9,%r13,8), %ymm2
   3bba2:      	vmovupd	(%r8,%r13,8), %ymm5
   3bba8:      	vaddpd	(%r15,%r13,8), %ymm1, %ymm3
   3bbae:      	vsubpd	(%r10,%r13,8), %ymm4, %ymm6
   3bbb4:      	vsubpd	%ymm6, %ymm3, %ymm7
   3bbb8:      	vfmadd213pd	%ymm7, %ymm0, %ymm4 # ymm4 = (ymm0 * ymm4) + ymm7
   3bbbd:      	vaddpd	(%r14,%r13,8), %ymm2, %ymm8
   3bbc3:      	vsubpd	(%r11,%r13,8), %ymm5, %ymm9
   3bbc9:      	vfmsub213pd	%ymm7, %ymm0, %ymm1 # ymm1 = (ymm0 * ymm1) - ymm7
   3bbce:      	vaddpd	%ymm9, %ymm8, %ymm7
   3bbd3:      	vfnmadd213pd	%ymm7, %ymm0, %ymm5 # ymm5 = -(ymm0 * ymm5) + ymm7
   3bbd8:      	vfmsub213pd	%ymm7, %ymm0, %ymm2 # ymm2 = (ymm0 * ymm2) - ymm7
   3bbdd:      	vaddpd	%ymm5, %ymm4, %ymm7
   3bbe1:      	vfnmadd213pd	%ymm7, %ymm0, %ymm8 # ymm8 = -(ymm0 * ymm8) + ymm7
   3bbe6:      	vfmsub213pd	%ymm7, %ymm0, %ymm3 # ymm3 = (ymm0 * ymm3) - ymm7
   3bbeb:      	vfmsub213pd	%ymm8, %ymm0, %ymm4 # ymm4 = (ymm0 * ymm4) - ymm8
   3bbf0:      	vfmadd213pd	%ymm3, %ymm0, %ymm5 # ymm5 = (ymm0 * ymm5) + ymm3
   3bbf5:      	vaddpd	%ymm2, %ymm1, %ymm7
   3bbf9:      	vfmadd213pd	%ymm7, %ymm0, %ymm9 # ymm9 = (ymm0 * ymm9) + ymm7
   3bbfe:      	vfnmadd213pd	%ymm7, %ymm0, %ymm6 # ymm6 = -(ymm0 * ymm6) + ymm7
   3bc03:      	vfmsub213pd	%ymm9, %ymm0, %ymm1 # ymm1 = (ymm0 * ymm1) - ymm9
   3bc08:      	vfnmadd213pd	%ymm6, %ymm0, %ymm2 # ymm2 = -(ymm0 * ymm2) + ymm6
   3bc0d:      	vmovupd	%ymm4, (%rdi,%r13,8)
   3bc13:      	vmovupd	%ymm9, (%r15,%r13,8)
   3bc19:      	vmovupd	%ymm5, (%rcx,%r13,8)
   3bc1f:      	vmovupd	%ymm6, (%r10,%r13,8)
   3bc25:      	vmovupd	%ymm8, (%r9,%r13,8)
   3bc2b:      	vmovupd	%ymm3, (%r14,%r13,8)
   3bc31:      	vmovupd	%ymm1, (%r8,%r13,8)
   3bc37:      	vmovupd	%ymm2, (%r11,%r13,8)
   3bc3d:      	addq	$0x4, %r13
   3bc41:      	cmpq	%rdx, %r13
   3bc44:      	jb	0x3bb90 <hstep_broken_g20+0x90>
   3bc4a:      	addq	%rax, %r12
   3bc4d:      	addq	%rbx, %r11
   3bc50:      	addq	%rbx, %r8
   3bc53:      	addq	%rbx, %r14
   3bc56:      	addq	%rbx, %r9
   3bc59:      	addq	%rbx, %r10
   3bc5c:      	addq	%rbx, %rcx
   3bc5f:      	addq	%rbx, %rdi
   3bc62:      	addq	%rbx, %r15
   3bc65:      	cmpq	%rsi, %r12
   3bc68:      	jb	0x3bb80 <hstep_broken_g20+0x80>
   3bc6e:      	popq	%rbx
   3bc6f:      	popq	%r12
   3bc71:      	popq	%r13
   3bc73:      	popq	%r14
   3bc75:      	popq	%r15
   3bc77:      	vzeroupper
   3bc7a:      	retq
   3bc7b:      	nopl	(%rax,%rax)

000000000003bc80 <hfirst_tb8_nat>:
   3bc80:      	vmovaps	(%rip), %ymm0           # 0x3bc88 <hfirst_tb8_nat+0x8>
   3bc88:      	testq	%rsi, %rsi
   3bc8b:      	je	0x3beb2 <hfirst_tb8_nat+0x232>
   3bc91:      	xorl	%eax, %eax
   3bc93:      	vxorpd	%xmm0, %xmm0, %xmm0
   3bc97:      	nopw	(%rax,%rax)
   3bca0:      	vmovupd	(%rdi,%rax,8), %ymm1
   3bca5:      	vmovupd	0x20(%rdi,%rax,8), %ymm2
   3bcab:      	vmovupd	0x40(%rdi,%rax,8), %ymm3
   3bcb1:      	vmovupd	0x60(%rdi,%rax,8), %ymm4
   3bcb7:      	vmovddup	%ymm1, %ymm5            # ymm5 = ymm1[0,0,2,2]
   3bcbb:      	vshufpd	$0xf, %ymm1, %ymm1, %ymm1 # ymm1 = ymm1[1,1,3,3]
   3bcc0:      	vsubpd	%ymm1, %ymm0, %ymm1
   3bcc4:      	vaddsubpd	%ymm1, %ymm5, %ymm1
   3bcc8:      	vpermpd	$0x44, %ymm1, %ymm5     # ymm5 = ymm1[0,1,0,1]
   3bcce:      	vsubpd	%ymm1, %ymm0, %ymm6
   3bcd2:      	vperm2f128	$0x31, %ymm6, %ymm1, %ymm1 # ymm1 = ymm1[2,3],ymm6[2,3]
   3bcd8:      	vaddpd	%ymm1, %ymm5, %ymm1
   3bcdc:      	vmovddup	%ymm2, %ymm5            # ymm5 = ymm2[0,0,2,2]
   3bce0:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3bce5:      	vsubpd	%ymm2, %ymm0, %ymm2
   3bce9:      	vaddsubpd	%ymm2, %ymm5, %ymm2
   3bced:      	vpermpd	$0x44, %ymm2, %ymm5     # ymm5 = ymm2[0,1,0,1]
   3bcf3:      	vsubpd	%ymm2, %ymm0, %ymm6
   3bcf7:      	vperm2f128	$0x31, %ymm6, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm6[2,3]
   3bcfd:      	vaddpd	%ymm2, %ymm5, %ymm2
   3bd01:      	vmovddup	%ymm3, %ymm5            # ymm5 = ymm3[0,0,2,2]
   3bd05:      	vshufpd	$0xf, %ymm3, %ymm3, %ymm3 # ymm3 = ymm3[1,1,3,3]
   3bd0a:      	vsubpd	%ymm3, %ymm0, %ymm3
   3bd0e:      	vaddsubpd	%ymm3, %ymm5, %ymm3
   3bd12:      	vpermpd	$0x44, %ymm3, %ymm5     # ymm5 = ymm3[0,1,0,1]
   3bd18:      	vsubpd	%ymm3, %ymm0, %ymm6
   3bd1c:      	vperm2f128	$0x31, %ymm6, %ymm3, %ymm3 # ymm3 = ymm3[2,3],ymm6[2,3]
   3bd22:      	vaddpd	%ymm3, %ymm5, %ymm3
   3bd26:      	vmovddup	%ymm4, %ymm5            # ymm5 = ymm4[0,0,2,2]
   3bd2a:      	vshufpd	$0xf, %ymm4, %ymm4, %ymm4 # ymm4 = ymm4[1,1,3,3]
   3bd2f:      	vsubpd	%ymm4, %ymm0, %ymm4
   3bd33:      	vaddsubpd	%ymm4, %ymm5, %ymm4
   3bd37:      	vpermpd	$0x44, %ymm4, %ymm5     # ymm5 = ymm4[0,1,0,1]
   3bd3d:      	vsubpd	%ymm4, %ymm0, %ymm6
   3bd41:      	vperm2f128	$0x31, %ymm6, %ymm4, %ymm4 # ymm4 = ymm4[2,3],ymm6[2,3]
   3bd47:      	vaddpd	%ymm4, %ymm5, %ymm4
   3bd4b:      	vmovupd	0x80(%rdi,%rax,8), %ymm5
   3bd54:      	vmovddup	%ymm5, %ymm6            # ymm6 = ymm5[0,0,2,2]
   3bd58:      	vshufpd	$0xf, %ymm5, %ymm5, %ymm5 # ymm5 = ymm5[1,1,3,3]
   3bd5d:      	vsubpd	%ymm5, %ymm0, %ymm5
   3bd61:      	vaddsubpd	%ymm5, %ymm6, %ymm5
   3bd65:      	vpermpd	$0x44, %ymm5, %ymm6     # ymm6 = ymm5[0,1,0,1]
   3bd6b:      	vsubpd	%ymm5, %ymm0, %ymm7
   3bd6f:      	vperm2f128	$0x31, %ymm7, %ymm5, %ymm5 # ymm5 = ymm5[2,3],ymm7[2,3]
   3bd75:      	vaddpd	%ymm5, %ymm6, %ymm5
   3bd79:      	vmovupd	0xa0(%rdi,%rax,8), %ymm6
   3bd82:      	vmovddup	%ymm6, %ymm7            # ymm7 = ymm6[0,0,2,2]
   3bd86:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm6 # ymm6 = ymm6[1,1,3,3]
   3bd8b:      	vsubpd	%ymm6, %ymm0, %ymm6
   3bd8f:      	vaddsubpd	%ymm6, %ymm7, %ymm6
   3bd93:      	vpermpd	$0x44, %ymm6, %ymm7     # ymm7 = ymm6[0,1,0,1]
   3bd99:      	vsubpd	%ymm6, %ymm0, %ymm8
   3bd9d:      	vperm2f128	$0x31, %ymm8, %ymm6, %ymm6 # ymm6 = ymm6[2,3],ymm8[2,3]
   3bda3:      	vaddpd	%ymm6, %ymm7, %ymm6
   3bda7:      	vmovupd	0xc0(%rdi,%rax,8), %ymm7
   3bdb0:      	vmovddup	%ymm7, %ymm8            # ymm8 = ymm7[0,0,2,2]
   3bdb4:      	vshufpd	$0xf, %ymm7, %ymm7, %ymm7 # ymm7 = ymm7[1,1,3,3]
   3bdb9:      	vsubpd	%ymm7, %ymm0, %ymm7
   3bdbd:      	vaddsubpd	%ymm7, %ymm8, %ymm7
   3bdc1:      	vpermpd	$0x44, %ymm7, %ymm8     # ymm8 = ymm7[0,1,0,1]
   3bdc7:      	vsubpd	%ymm7, %ymm0, %ymm9
   3bdcb:      	vperm2f128	$0x31, %ymm9, %ymm7, %ymm7 # ymm7 = ymm7[2,3],ymm9[2,3]
   3bdd1:      	vaddpd	%ymm7, %ymm8, %ymm7
   3bdd5:      	vmovupd	0xe0(%rdi,%rax,8), %ymm8
   3bdde:      	vmovddup	%ymm8, %ymm9            # ymm9 = ymm8[0,0,2,2]
   3bde3:      	vshufpd	$0xf, %ymm8, %ymm8, %ymm8 # ymm8 = ymm8[1,1,3,3]
   3bde9:      	vsubpd	%ymm8, %ymm0, %ymm8
   3bdee:      	vaddsubpd	%ymm8, %ymm9, %ymm8
   3bdf3:      	vpermpd	$0x44, %ymm8, %ymm9     # ymm9 = ymm8[0,1,0,1]
   3bdf9:      	vsubpd	%ymm8, %ymm0, %ymm10
   3bdfe:      	vperm2f128	$0x31, %ymm10, %ymm8, %ymm8 # ymm8 = ymm8[2,3],ymm10[2,3]
   3be04:      	vaddpd	%ymm8, %ymm9, %ymm8
   3be09:      	vaddpd	%ymm2, %ymm1, %ymm9
   3be0d:      	vsubpd	%ymm2, %ymm1, %ymm1
   3be11:      	vaddpd	%ymm4, %ymm3, %ymm2
   3be15:      	vsubpd	%ymm4, %ymm3, %ymm3
   3be19:      	vaddpd	%ymm6, %ymm5, %ymm4
   3be1d:      	vsubpd	%ymm6, %ymm5, %ymm5
   3be21:      	vaddpd	%ymm7, %ymm8, %ymm6
   3be25:      	vsubpd	%ymm8, %ymm7, %ymm7
   3be2a:      	vaddpd	%ymm2, %ymm9, %ymm8
   3be2e:      	vsubpd	%ymm2, %ymm9, %ymm2
   3be32:      	vaddpd	%ymm3, %ymm1, %ymm9
   3be36:      	vsubpd	%ymm3, %ymm1, %ymm1
   3be3a:      	vaddpd	%ymm6, %ymm4, %ymm3
   3be3e:      	vsubpd	%ymm6, %ymm4, %ymm4
   3be42:      	vaddpd	%ymm7, %ymm5, %ymm6
   3be46:      	vsubpd	%ymm7, %ymm5, %ymm5
   3be4a:      	vaddpd	%ymm3, %ymm8, %ymm7
   3be4e:      	vsubpd	%ymm3, %ymm8, %ymm3
   3be52:      	vaddpd	%ymm6, %ymm9, %ymm8
   3be56:      	vsubpd	%ymm6, %ymm9, %ymm6
   3be5a:      	vaddpd	%ymm4, %ymm2, %ymm9
   3be5e:      	vsubpd	%ymm4, %ymm2, %ymm2
   3be62:      	vaddpd	%ymm5, %ymm1, %ymm4
   3be66:      	vsubpd	%ymm5, %ymm1, %ymm1
   3be6a:      	vmovupd	%ymm7, (%rdi,%rax,8)
   3be6f:      	vmovupd	%ymm8, 0x20(%rdi,%rax,8)
   3be75:      	vmovupd	%ymm9, 0x40(%rdi,%rax,8)
   3be7b:      	vmovupd	%ymm4, 0x60(%rdi,%rax,8)
   3be81:      	vmovupd	%ymm3, 0x80(%rdi,%rax,8)
   3be8a:      	vmovupd	%ymm6, 0xa0(%rdi,%rax,8)
   3be93:      	vmovupd	%ymm2, 0xc0(%rdi,%rax,8)
   3be9c:      	vmovupd	%ymm1, 0xe0(%rdi,%rax,8)
   3bea5:      	addq	$0x20, %rax
   3bea9:      	cmpq	%rsi, %rax
   3beac:      	jb	0x3bca0 <hfirst_tb8_nat+0x20>
   3beb2:      	vzeroupper
   3beb5:      	retq
   3beb6:      	nopw	%cs:(%rax,%rax)

000000000003bec0 <hstep_tb8_nat>:
   3bec0:      	pushq	%r15
   3bec2:      	pushq	%r14
   3bec4:      	pushq	%r13
   3bec6:      	pushq	%r12
   3bec8:      	pushq	%rbx
   3bec9:      	vmovaps	(%rip), %ymm0           # 0x3bed1 <hstep_tb8_nat+0x11>
   3bed1:      	testq	%rsi, %rsi
   3bed4:      	je	0x3c031 <hstep_tb8_nat+0x171>
   3beda:      	testq	%rdx, %rdx
   3bedd:      	je	0x3c031 <hstep_tb8_nat+0x171>
   3bee3:      	leaq	(,%rdx,8), %rax
   3beeb:      	movq	%rdx, %rcx
   3beee:      	shlq	$0x4, %rcx
   3bef2:      	leaq	(%rdx,%rdx,2), %r8
   3bef6:      	movq	%rdx, %r9
   3bef9:      	shlq	$0x5, %r9
   3befd:      	leaq	(%rdx,%rdx,4), %r14
   3bf01:      	leaq	(%rdi,%r8,8), %r10
   3bf05:      	shlq	$0x4, %r8
   3bf09:      	imulq	$0x38, %rdx, %r11
   3bf0d:      	addq	%rdi, %r11
   3bf10:      	movq	%rdx, %rbx
   3bf13:      	shlq	$0x6, %rbx
   3bf17:      	addq	%rdi, %r8
   3bf1a:      	leaq	(%rdi,%r14,8), %r14
   3bf1e:      	addq	%rdi, %r9
   3bf21:      	addq	%rdi, %rcx
   3bf24:      	leaq	(%rdi,%rax), %r15
   3bf28:      	xorl	%r12d, %r12d
   3bf2b:      	nopl	(%rax,%rax)
   3bf30:      	xorl	%r13d, %r13d
   3bf33:      	nopw	%cs:(%rax,%rax)
   3bf40:      	vmovupd	(%rdi,%r13,8), %ymm0
   3bf46:      	vmovupd	(%r15,%r13,8), %ymm1
   3bf4c:      	vmovupd	(%rcx,%r13,8), %ymm2
   3bf52:      	vmovupd	(%r10,%r13,8), %ymm3
   3bf58:      	vmovupd	(%r9,%r13,8), %ymm4
   3bf5e:      	vmovupd	(%r14,%r13,8), %ymm5
   3bf64:      	vmovupd	(%r8,%r13,8), %ymm6
   3bf6a:      	vmovupd	(%r11,%r13,8), %ymm7
   3bf70:      	vaddpd	%ymm1, %ymm0, %ymm8
   3bf74:      	vsubpd	%ymm1, %ymm0, %ymm0
   3bf78:      	vaddpd	%ymm3, %ymm2, %ymm1
   3bf7c:      	vsubpd	%ymm3, %ymm2, %ymm2
   3bf80:      	vaddpd	%ymm5, %ymm4, %ymm3
   3bf84:      	vsubpd	%ymm5, %ymm4, %ymm4
   3bf88:      	vaddpd	%ymm7, %ymm6, %ymm5
   3bf8c:      	vsubpd	%ymm7, %ymm6, %ymm6
   3bf90:      	vaddpd	%ymm1, %ymm8, %ymm7
   3bf94:      	vsubpd	%ymm1, %ymm8, %ymm1
   3bf98:      	vaddpd	%ymm2, %ymm0, %ymm8
   3bf9c:      	vsubpd	%ymm2, %ymm0, %ymm0
   3bfa0:      	vaddpd	%ymm5, %ymm3, %ymm2
   3bfa4:      	vsubpd	%ymm5, %ymm3, %ymm3
   3bfa8:      	vaddpd	%ymm6, %ymm4, %ymm5
   3bfac:      	vsubpd	%ymm6, %ymm4, %ymm4
   3bfb0:      	vaddpd	%ymm2, %ymm7, %ymm6
   3bfb4:      	vsubpd	%ymm2, %ymm7, %ymm2
   3bfb8:      	vaddpd	%ymm5, %ymm8, %ymm7
   3bfbc:      	vsubpd	%ymm5, %ymm8, %ymm5
   3bfc0:      	vaddpd	%ymm3, %ymm1, %ymm8
   3bfc4:      	vsubpd	%ymm3, %ymm1, %ymm1
   3bfc8:      	vaddpd	%ymm4, %ymm0, %ymm3
   3bfcc:      	vsubpd	%ymm4, %ymm0, %ymm0
   3bfd0:      	vmovupd	%ymm6, (%rdi,%r13,8)
   3bfd6:      	vmovupd	%ymm7, (%r15,%r13,8)
   3bfdc:      	vmovupd	%ymm8, (%rcx,%r13,8)
   3bfe2:      	vmovupd	%ymm3, (%r10,%r13,8)
   3bfe8:      	vmovupd	%ymm2, (%r9,%r13,8)
   3bfee:      	vmovupd	%ymm5, (%r14,%r13,8)
   3bff4:      	vmovupd	%ymm1, (%r8,%r13,8)
   3bffa:      	vmovupd	%ymm0, (%r11,%r13,8)
   3c000:      	addq	$0x4, %r13
   3c004:      	cmpq	%rdx, %r13
   3c007:      	jb	0x3bf40 <hstep_tb8_nat+0x80>
   3c00d:      	addq	%rax, %r12
   3c010:      	addq	%rbx, %r11
   3c013:      	addq	%rbx, %r8
   3c016:      	addq	%rbx, %r14
   3c019:      	addq	%rbx, %r9
   3c01c:      	addq	%rbx, %r10
   3c01f:      	addq	%rbx, %rcx
   3c022:      	addq	%rbx, %rdi
   3c025:      	addq	%rbx, %r15
   3c028:      	cmpq	%rsi, %r12
   3c02b:      	jb	0x3bf30 <hstep_tb8_nat+0x70>
   3c031:      	popq	%rbx
   3c032:      	popq	%r12
   3c034:      	popq	%r13
   3c036:      	popq	%r14
   3c038:      	popq	%r15
   3c03a:      	vzeroupper
   3c03d:      	retq
   3c03e:      	nop

000000000003c040 <hfirst_tb8_bal>:
   3c040:      	vmovaps	(%rip), %ymm0           # 0x3c048 <hfirst_tb8_bal+0x8>
   3c048:      	testq	%rsi, %rsi
   3c04b:      	je	0x3c2b5 <hfirst_tb8_bal+0x275>
   3c051:      	xorl	%eax, %eax
   3c053:      	vxorpd	%xmm1, %xmm1, %xmm1
   3c057:      	nopw	(%rax,%rax)
   3c060:      	vmovupd	(%rdi,%rax,8), %ymm2
   3c065:      	vmovupd	0x20(%rdi,%rax,8), %ymm3
   3c06b:      	vmovupd	0x40(%rdi,%rax,8), %ymm4
   3c071:      	vmovupd	0x60(%rdi,%rax,8), %ymm5
   3c077:      	vmovddup	%ymm2, %ymm6            # ymm6 = ymm2[0,0,2,2]
   3c07b:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3c080:      	vsubpd	%ymm2, %ymm1, %ymm2
   3c084:      	vaddsubpd	%ymm2, %ymm6, %ymm2
   3c088:      	vpermpd	$0x44, %ymm2, %ymm6     # ymm6 = ymm2[0,1,0,1]
   3c08e:      	vsubpd	%ymm2, %ymm1, %ymm7
   3c092:      	vperm2f128	$0x31, %ymm7, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm7[2,3]
   3c098:      	vaddpd	%ymm2, %ymm6, %ymm2
   3c09c:      	vmovddup	%ymm3, %ymm6            # ymm6 = ymm3[0,0,2,2]
   3c0a0:      	vshufpd	$0xf, %ymm3, %ymm3, %ymm3 # ymm3 = ymm3[1,1,3,3]
   3c0a5:      	vsubpd	%ymm3, %ymm1, %ymm3
   3c0a9:      	vaddsubpd	%ymm3, %ymm6, %ymm3
   3c0ad:      	vpermpd	$0x44, %ymm3, %ymm6     # ymm6 = ymm3[0,1,0,1]
   3c0b3:      	vsubpd	%ymm3, %ymm1, %ymm7
   3c0b7:      	vperm2f128	$0x31, %ymm7, %ymm3, %ymm3 # ymm3 = ymm3[2,3],ymm7[2,3]
   3c0bd:      	vaddpd	%ymm3, %ymm6, %ymm3
   3c0c1:      	vmovddup	%ymm4, %ymm6            # ymm6 = ymm4[0,0,2,2]
   3c0c5:      	vshufpd	$0xf, %ymm4, %ymm4, %ymm4 # ymm4 = ymm4[1,1,3,3]
   3c0ca:      	vsubpd	%ymm4, %ymm1, %ymm4
   3c0ce:      	vaddsubpd	%ymm4, %ymm6, %ymm4
   3c0d2:      	vpermpd	$0x44, %ymm4, %ymm6     # ymm6 = ymm4[0,1,0,1]
   3c0d8:      	vsubpd	%ymm4, %ymm1, %ymm7
   3c0dc:      	vperm2f128	$0x31, %ymm7, %ymm4, %ymm4 # ymm4 = ymm4[2,3],ymm7[2,3]
   3c0e2:      	vaddpd	%ymm4, %ymm6, %ymm4
   3c0e6:      	vmovddup	%ymm5, %ymm6            # ymm6 = ymm5[0,0,2,2]
   3c0ea:      	vshufpd	$0xf, %ymm5, %ymm5, %ymm5 # ymm5 = ymm5[1,1,3,3]
   3c0ef:      	vsubpd	%ymm5, %ymm1, %ymm5
   3c0f3:      	vaddsubpd	%ymm5, %ymm6, %ymm5
   3c0f7:      	vpermpd	$0x44, %ymm5, %ymm6     # ymm6 = ymm5[0,1,0,1]
   3c0fd:      	vsubpd	%ymm5, %ymm1, %ymm7
   3c101:      	vperm2f128	$0x31, %ymm7, %ymm5, %ymm5 # ymm5 = ymm5[2,3],ymm7[2,3]
   3c107:      	vaddpd	%ymm5, %ymm6, %ymm5
   3c10b:      	vmovupd	0x80(%rdi,%rax,8), %ymm6
   3c114:      	vmovddup	%ymm6, %ymm7            # ymm7 = ymm6[0,0,2,2]
   3c118:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm6 # ymm6 = ymm6[1,1,3,3]
   3c11d:      	vsubpd	%ymm6, %ymm1, %ymm6
   3c121:      	vaddsubpd	%ymm6, %ymm7, %ymm6
   3c125:      	vpermpd	$0x44, %ymm6, %ymm7     # ymm7 = ymm6[0,1,0,1]
   3c12b:      	vsubpd	%ymm6, %ymm1, %ymm8
   3c12f:      	vperm2f128	$0x31, %ymm8, %ymm6, %ymm6 # ymm6 = ymm6[2,3],ymm8[2,3]
   3c135:      	vaddpd	%ymm6, %ymm7, %ymm6
   3c139:      	vmovupd	0xa0(%rdi,%rax,8), %ymm7
   3c142:      	vmovddup	%ymm7, %ymm8            # ymm8 = ymm7[0,0,2,2]
   3c146:      	vshufpd	$0xf, %ymm7, %ymm7, %ymm7 # ymm7 = ymm7[1,1,3,3]
   3c14b:      	vsubpd	%ymm7, %ymm1, %ymm7
   3c14f:      	vaddsubpd	%ymm7, %ymm8, %ymm7
   3c153:      	vpermpd	$0x44, %ymm7, %ymm8     # ymm8 = ymm7[0,1,0,1]
   3c159:      	vsubpd	%ymm7, %ymm1, %ymm9
   3c15d:      	vperm2f128	$0x31, %ymm9, %ymm7, %ymm7 # ymm7 = ymm7[2,3],ymm9[2,3]
   3c163:      	vaddpd	%ymm7, %ymm8, %ymm7
   3c167:      	vmovupd	0xc0(%rdi,%rax,8), %ymm8
   3c170:      	vmovddup	%ymm8, %ymm9            # ymm9 = ymm8[0,0,2,2]
   3c175:      	vshufpd	$0xf, %ymm8, %ymm8, %ymm8 # ymm8 = ymm8[1,1,3,3]
   3c17b:      	vsubpd	%ymm8, %ymm1, %ymm8
   3c180:      	vaddsubpd	%ymm8, %ymm9, %ymm8
   3c185:      	vpermpd	$0x44, %ymm8, %ymm9     # ymm9 = ymm8[0,1,0,1]
   3c18b:      	vsubpd	%ymm8, %ymm1, %ymm10
   3c190:      	vperm2f128	$0x31, %ymm10, %ymm8, %ymm8 # ymm8 = ymm8[2,3],ymm10[2,3]
   3c196:      	vaddpd	%ymm8, %ymm9, %ymm8
   3c19b:      	vmovupd	0xe0(%rdi,%rax,8), %ymm9
   3c1a4:      	vmovddup	%ymm9, %ymm10           # ymm10 = ymm9[0,0,2,2]
   3c1a9:      	vshufpd	$0xf, %ymm9, %ymm9, %ymm9 # ymm9 = ymm9[1,1,3,3]
   3c1af:      	vsubpd	%ymm9, %ymm1, %ymm9
   3c1b4:      	vaddsubpd	%ymm9, %ymm10, %ymm9
   3c1b9:      	vpermpd	$0x44, %ymm9, %ymm10    # ymm10 = ymm9[0,1,0,1]
   3c1bf:      	vsubpd	%ymm9, %ymm1, %ymm11
   3c1c4:      	vperm2f128	$0x31, %ymm11, %ymm9, %ymm9 # ymm9 = ymm9[2,3],ymm11[2,3]
   3c1ca:      	vaddpd	%ymm9, %ymm10, %ymm9
   3c1cf:      	vmovapd	%ymm0, %ymm10
   3c1d3:      	vfmadd213pd	%ymm2, %ymm3, %ymm10 # ymm10 = (ymm3 * ymm10) + ymm2
   3c1d8:      	vsubpd	%ymm3, %ymm2, %ymm2
   3c1dc:      	vmovapd	%ymm0, %ymm3
   3c1e0:      	vfmadd213pd	%ymm4, %ymm5, %ymm3 # ymm3 = (ymm5 * ymm3) + ymm4
   3c1e5:      	vsubpd	%ymm5, %ymm4, %ymm4
   3c1e9:      	vmovapd	%ymm0, %ymm5
   3c1ed:      	vfmadd213pd	%ymm6, %ymm7, %ymm5 # ymm5 = (ymm7 * ymm5) + ymm6
   3c1f2:      	vsubpd	%ymm7, %ymm6, %ymm6
   3c1f6:      	vmovapd	%ymm0, %ymm7
   3c1fa:      	vfmadd213pd	%ymm8, %ymm9, %ymm7 # ymm7 = (ymm9 * ymm7) + ymm8
   3c1ff:      	vsubpd	%ymm9, %ymm8, %ymm8
   3c204:      	vmovapd	%ymm0, %ymm9
   3c208:      	vfmadd213pd	%ymm10, %ymm3, %ymm9 # ymm9 = (ymm3 * ymm9) + ymm10
   3c20d:      	vsubpd	%ymm3, %ymm10, %ymm3
   3c211:      	vmovapd	%ymm0, %ymm10
   3c215:      	vfmadd213pd	%ymm2, %ymm4, %ymm10 # ymm10 = (ymm4 * ymm10) + ymm2
   3c21a:      	vsubpd	%ymm4, %ymm2, %ymm2
   3c21e:      	vmovapd	%ymm0, %ymm4
   3c222:      	vfmadd213pd	%ymm5, %ymm7, %ymm4 # ymm4 = (ymm7 * ymm4) + ymm5
   3c227:      	vsubpd	%ymm7, %ymm5, %ymm5
   3c22b:      	vmovapd	%ymm0, %ymm7
   3c22f:      	vfmadd213pd	%ymm6, %ymm8, %ymm7 # ymm7 = (ymm8 * ymm7) + ymm6
   3c234:      	vsubpd	%ymm8, %ymm6, %ymm6
   3c239:      	vmovapd	%ymm0, %ymm8
   3c23d:      	vfmadd213pd	%ymm9, %ymm4, %ymm8 # ymm8 = (ymm4 * ymm8) + ymm9
   3c242:      	vsubpd	%ymm4, %ymm9, %ymm4
   3c246:      	vmovapd	%ymm0, %ymm9
   3c24a:      	vfmadd213pd	%ymm10, %ymm7, %ymm9 # ymm9 = (ymm7 * ymm9) + ymm10
   3c24f:      	vsubpd	%ymm7, %ymm10, %ymm7
   3c253:      	vmovapd	%ymm0, %ymm10
   3c257:      	vfmadd213pd	%ymm3, %ymm5, %ymm10 # ymm10 = (ymm5 * ymm10) + ymm3
   3c25c:      	vsubpd	%ymm5, %ymm3, %ymm3
   3c260:      	vmovapd	%ymm0, %ymm5
   3c264:      	vfmadd213pd	%ymm2, %ymm6, %ymm5 # ymm5 = (ymm6 * ymm5) + ymm2
   3c269:      	vsubpd	%ymm6, %ymm2, %ymm2
   3c26d:      	vmovupd	%ymm8, (%rdi,%rax,8)
   3c272:      	vmovupd	%ymm9, 0x20(%rdi,%rax,8)
   3c278:      	vmovupd	%ymm10, 0x40(%rdi,%rax,8)
   3c27e:      	vmovupd	%ymm5, 0x60(%rdi,%rax,8)
   3c284:      	vmovupd	%ymm4, 0x80(%rdi,%rax,8)
   3c28d:      	vmovupd	%ymm7, 0xa0(%rdi,%rax,8)
   3c296:      	vmovupd	%ymm3, 0xc0(%rdi,%rax,8)
   3c29f:      	vmovupd	%ymm2, 0xe0(%rdi,%rax,8)
   3c2a8:      	addq	$0x20, %rax
   3c2ac:      	cmpq	%rsi, %rax
   3c2af:      	jb	0x3c060 <hfirst_tb8_bal+0x20>
   3c2b5:      	vzeroupper
   3c2b8:      	retq
   3c2b9:      	nopl	(%rax)

000000000003c2c0 <hstep_tb8_bal>:
   3c2c0:      	pushq	%r15
   3c2c2:      	pushq	%r14
   3c2c4:      	pushq	%r13
   3c2c6:      	pushq	%r12
   3c2c8:      	pushq	%rbx
   3c2c9:      	vmovaps	(%rip), %ymm0           # 0x3c2d1 <hstep_tb8_bal+0x11>
   3c2d1:      	testq	%rsi, %rsi
   3c2d4:      	je	0x3c46e <hstep_tb8_bal+0x1ae>
   3c2da:      	testq	%rdx, %rdx
   3c2dd:      	je	0x3c46e <hstep_tb8_bal+0x1ae>
   3c2e3:      	leaq	(,%rdx,8), %rax
   3c2eb:      	movq	%rdx, %rcx
   3c2ee:      	shlq	$0x4, %rcx
   3c2f2:      	leaq	(%rdx,%rdx,2), %r8
   3c2f6:      	movq	%rdx, %r9
   3c2f9:      	shlq	$0x5, %r9
   3c2fd:      	leaq	(%rdx,%rdx,4), %r14
   3c301:      	leaq	(%rdi,%r8,8), %r10
   3c305:      	shlq	$0x4, %r8
   3c309:      	imulq	$0x38, %rdx, %r11
   3c30d:      	addq	%rdi, %r11
   3c310:      	movq	%rdx, %rbx
   3c313:      	shlq	$0x6, %rbx
   3c317:      	addq	%rdi, %r8
   3c31a:      	leaq	(%rdi,%r14,8), %r14
   3c31e:      	addq	%rdi, %r9
   3c321:      	addq	%rdi, %rcx
   3c324:      	leaq	(%rdi,%rax), %r15
   3c328:      	xorl	%r12d, %r12d
   3c32b:      	nopl	(%rax,%rax)
   3c330:      	xorl	%r13d, %r13d
   3c333:      	nopw	%cs:(%rax,%rax)
   3c340:      	vmovupd	(%rdi,%r13,8), %ymm1
   3c346:      	vmovupd	(%r15,%r13,8), %ymm2
   3c34c:      	vmovupd	(%rcx,%r13,8), %ymm3
   3c352:      	vmovupd	(%r10,%r13,8), %ymm4
   3c358:      	vmovupd	(%r9,%r13,8), %ymm5
   3c35e:      	vmovupd	(%r14,%r13,8), %ymm6
   3c364:      	vmovupd	(%r8,%r13,8), %ymm7
   3c36a:      	vmovupd	(%r11,%r13,8), %ymm8
   3c370:      	vmovapd	%ymm0, %ymm9
   3c374:      	vfmadd213pd	%ymm1, %ymm2, %ymm9 # ymm9 = (ymm2 * ymm9) + ymm1
   3c379:      	vsubpd	%ymm2, %ymm1, %ymm1
   3c37d:      	vmovapd	%ymm0, %ymm2
   3c381:      	vfmadd213pd	%ymm3, %ymm4, %ymm2 # ymm2 = (ymm4 * ymm2) + ymm3
   3c386:      	vsubpd	%ymm4, %ymm3, %ymm3
   3c38a:      	vmovapd	%ymm0, %ymm4
   3c38e:      	vfmadd213pd	%ymm5, %ymm6, %ymm4 # ymm4 = (ymm6 * ymm4) + ymm5
   3c393:      	vsubpd	%ymm6, %ymm5, %ymm5
   3c397:      	vmovapd	%ymm0, %ymm6
   3c39b:      	vfmadd213pd	%ymm7, %ymm8, %ymm6 # ymm6 = (ymm8 * ymm6) + ymm7
   3c3a0:      	vsubpd	%ymm8, %ymm7, %ymm7
   3c3a5:      	vmovapd	%ymm0, %ymm8
   3c3a9:      	vfmadd213pd	%ymm9, %ymm2, %ymm8 # ymm8 = (ymm2 * ymm8) + ymm9
   3c3ae:      	vsubpd	%ymm2, %ymm9, %ymm2
   3c3b2:      	vmovapd	%ymm0, %ymm9
   3c3b6:      	vfmadd213pd	%ymm1, %ymm3, %ymm9 # ymm9 = (ymm3 * ymm9) + ymm1
   3c3bb:      	vsubpd	%ymm3, %ymm1, %ymm1
   3c3bf:      	vmovapd	%ymm0, %ymm3
   3c3c3:      	vfmadd213pd	%ymm4, %ymm6, %ymm3 # ymm3 = (ymm6 * ymm3) + ymm4
   3c3c8:      	vsubpd	%ymm6, %ymm4, %ymm4
   3c3cc:      	vmovapd	%ymm0, %ymm6
   3c3d0:      	vfmadd213pd	%ymm5, %ymm7, %ymm6 # ymm6 = (ymm7 * ymm6) + ymm5
   3c3d5:      	vsubpd	%ymm7, %ymm5, %ymm5
   3c3d9:      	vmovapd	%ymm0, %ymm7
   3c3dd:      	vfmadd213pd	%ymm8, %ymm3, %ymm7 # ymm7 = (ymm3 * ymm7) + ymm8
   3c3e2:      	vsubpd	%ymm3, %ymm8, %ymm3
   3c3e6:      	vmovapd	%ymm0, %ymm8
   3c3ea:      	vfmadd213pd	%ymm9, %ymm6, %ymm8 # ymm8 = (ymm6 * ymm8) + ymm9
   3c3ef:      	vsubpd	%ymm6, %ymm9, %ymm6
   3c3f3:      	vmovapd	%ymm0, %ymm9
   3c3f7:      	vfmadd213pd	%ymm2, %ymm4, %ymm9 # ymm9 = (ymm4 * ymm9) + ymm2
   3c3fc:      	vsubpd	%ymm4, %ymm2, %ymm2
   3c400:      	vmovapd	%ymm0, %ymm4
   3c404:      	vfmadd213pd	%ymm1, %ymm5, %ymm4 # ymm4 = (ymm5 * ymm4) + ymm1
   3c409:      	vsubpd	%ymm5, %ymm1, %ymm1
   3c40d:      	vmovupd	%ymm7, (%rdi,%r13,8)
   3c413:      	vmovupd	%ymm8, (%r15,%r13,8)
   3c419:      	vmovupd	%ymm9, (%rcx,%r13,8)
   3c41f:      	vmovupd	%ymm4, (%r10,%r13,8)
   3c425:      	vmovupd	%ymm3, (%r9,%r13,8)
   3c42b:      	vmovupd	%ymm6, (%r14,%r13,8)
   3c431:      	vmovupd	%ymm2, (%r8,%r13,8)
   3c437:      	vmovupd	%ymm1, (%r11,%r13,8)
   3c43d:      	addq	$0x4, %r13
   3c441:      	cmpq	%rdx, %r13
   3c444:      	jb	0x3c340 <hstep_tb8_bal+0x80>
   3c44a:      	addq	%rax, %r12
   3c44d:      	addq	%rbx, %r11
   3c450:      	addq	%rbx, %r8
   3c453:      	addq	%rbx, %r14
   3c456:      	addq	%rbx, %r9
   3c459:      	addq	%rbx, %r10
   3c45c:      	addq	%rbx, %rcx
   3c45f:      	addq	%rbx, %rdi
   3c462:      	addq	%rbx, %r15
   3c465:      	cmpq	%rsi, %r12
   3c468:      	jb	0x3c330 <hstep_tb8_bal+0x70>
   3c46e:      	popq	%rbx
   3c46f:      	popq	%r12
   3c471:      	popq	%r13
   3c473:      	popq	%r14
   3c475:      	popq	%r15
   3c477:      	vzeroupper
   3c47a:      	retq
   3c47b:      	nopl	(%rax,%rax)

000000000003c480 <hfirst_tb16_nat>:
   3c480:      	subq	$0x68, %rsp
   3c484:      	vmovaps	(%rip), %ymm0           # 0x3c48c <hfirst_tb16_nat+0xc>
   3c48c:      	testq	%rsi, %rsi
   3c48f:      	je	0x3c9cd <hfirst_tb16_nat+0x54d>
   3c495:      	xorl	%eax, %eax
   3c497:      	nopw	(%rax,%rax)
   3c4a0:      	vmovupd	(%rdi,%rax,8), %ymm1
   3c4a5:      	vmovupd	0x20(%rdi,%rax,8), %ymm2
   3c4ab:      	vmovupd	0x40(%rdi,%rax,8), %ymm3
   3c4b1:      	vmovupd	0x60(%rdi,%rax,8), %ymm4
   3c4b7:      	vmovddup	%ymm1, %ymm5            # ymm5 = ymm1[0,0,2,2]
   3c4bb:      	vshufpd	$0xf, %ymm1, %ymm1, %ymm1 # ymm1 = ymm1[1,1,3,3]
   3c4c0:      	vxorpd	%xmm0, %xmm0, %xmm0
   3c4c4:      	vsubpd	%ymm1, %ymm0, %ymm1
   3c4c8:      	vaddsubpd	%ymm1, %ymm5, %ymm1
   3c4cc:      	vpermpd	$0x44, %ymm1, %ymm5     # ymm5 = ymm1[0,1,0,1]
   3c4d2:      	vsubpd	%ymm1, %ymm0, %ymm6
   3c4d6:      	vperm2f128	$0x31, %ymm6, %ymm1, %ymm1 # ymm1 = ymm1[2,3],ymm6[2,3]
   3c4dc:      	vaddpd	%ymm1, %ymm5, %ymm1
   3c4e0:      	vmovupd	%ymm1, -0x60(%rsp)
   3c4e6:      	vmovddup	%ymm2, %ymm5            # ymm5 = ymm2[0,0,2,2]
   3c4ea:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3c4ef:      	vsubpd	%ymm2, %ymm0, %ymm2
   3c4f3:      	vaddsubpd	%ymm2, %ymm5, %ymm2
   3c4f7:      	vpermpd	$0x44, %ymm2, %ymm5     # ymm5 = ymm2[0,1,0,1]
   3c4fd:      	vsubpd	%ymm2, %ymm0, %ymm6
   3c501:      	vperm2f128	$0x31, %ymm6, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm6[2,3]
   3c507:      	vaddpd	%ymm2, %ymm5, %ymm1
   3c50b:      	vmovupd	%ymm1, -0x80(%rsp)
   3c511:      	vmovddup	%ymm3, %ymm5            # ymm5 = ymm3[0,0,2,2]
   3c515:      	vshufpd	$0xf, %ymm3, %ymm3, %ymm3 # ymm3 = ymm3[1,1,3,3]
   3c51a:      	vsubpd	%ymm3, %ymm0, %ymm3
   3c51e:      	vaddsubpd	%ymm3, %ymm5, %ymm3
   3c522:      	vpermpd	$0x44, %ymm3, %ymm5     # ymm5 = ymm3[0,1,0,1]
   3c528:      	vsubpd	%ymm3, %ymm0, %ymm6
   3c52c:      	vperm2f128	$0x31, %ymm6, %ymm3, %ymm3 # ymm3 = ymm3[2,3],ymm6[2,3]
   3c532:      	vaddpd	%ymm3, %ymm5, %ymm1
   3c536:      	vmovupd	%ymm1, 0x40(%rsp)
   3c53c:      	vmovddup	%ymm4, %ymm5            # ymm5 = ymm4[0,0,2,2]
   3c540:      	vshufpd	$0xf, %ymm4, %ymm4, %ymm4 # ymm4 = ymm4[1,1,3,3]
   3c545:      	vsubpd	%ymm4, %ymm0, %ymm4
   3c549:      	vaddsubpd	%ymm4, %ymm5, %ymm4
   3c54d:      	vpermpd	$0x44, %ymm4, %ymm5     # ymm5 = ymm4[0,1,0,1]
   3c553:      	vsubpd	%ymm4, %ymm0, %ymm6
   3c557:      	vperm2f128	$0x31, %ymm6, %ymm4, %ymm4 # ymm4 = ymm4[2,3],ymm6[2,3]
   3c55d:      	vaddpd	%ymm4, %ymm5, %ymm4
   3c561:      	vmovupd	0x80(%rdi,%rax,8), %ymm5
   3c56a:      	vmovddup	%ymm5, %ymm6            # ymm6 = ymm5[0,0,2,2]
   3c56e:      	vshufpd	$0xf, %ymm5, %ymm5, %ymm5 # ymm5 = ymm5[1,1,3,3]
   3c573:      	vsubpd	%ymm5, %ymm0, %ymm5
   3c577:      	vaddsubpd	%ymm5, %ymm6, %ymm5
   3c57b:      	vpermpd	$0x44, %ymm5, %ymm6     # ymm6 = ymm5[0,1,0,1]
   3c581:      	vsubpd	%ymm5, %ymm0, %ymm7
   3c585:      	vperm2f128	$0x31, %ymm7, %ymm5, %ymm5 # ymm5 = ymm5[2,3],ymm7[2,3]
   3c58b:      	vaddpd	%ymm5, %ymm6, %ymm1
   3c58f:      	vmovupd	%ymm1, 0x20(%rsp)
   3c595:      	vmovupd	0xa0(%rdi,%rax,8), %ymm6
   3c59e:      	vmovddup	%ymm6, %ymm7            # ymm7 = ymm6[0,0,2,2]
   3c5a2:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm6 # ymm6 = ymm6[1,1,3,3]
   3c5a7:      	vsubpd	%ymm6, %ymm0, %ymm6
   3c5ab:      	vaddsubpd	%ymm6, %ymm7, %ymm6
   3c5af:      	vpermpd	$0x44, %ymm6, %ymm7     # ymm7 = ymm6[0,1,0,1]
   3c5b5:      	vsubpd	%ymm6, %ymm0, %ymm8
   3c5b9:      	vperm2f128	$0x31, %ymm8, %ymm6, %ymm6 # ymm6 = ymm6[2,3],ymm8[2,3]
   3c5bf:      	vaddpd	%ymm6, %ymm7, %ymm2
   3c5c3:      	vmovupd	0xc0(%rdi,%rax,8), %ymm7
   3c5cc:      	vmovddup	%ymm7, %ymm8            # ymm8 = ymm7[0,0,2,2]
   3c5d0:      	vshufpd	$0xf, %ymm7, %ymm7, %ymm7 # ymm7 = ymm7[1,1,3,3]
   3c5d5:      	vsubpd	%ymm7, %ymm0, %ymm7
   3c5d9:      	vaddsubpd	%ymm7, %ymm8, %ymm7
   3c5dd:      	vpermpd	$0x44, %ymm7, %ymm8     # ymm8 = ymm7[0,1,0,1]
   3c5e3:      	vsubpd	%ymm7, %ymm0, %ymm9
   3c5e7:      	vperm2f128	$0x31, %ymm9, %ymm7, %ymm7 # ymm7 = ymm7[2,3],ymm9[2,3]
   3c5ed:      	vaddpd	%ymm7, %ymm8, %ymm1
   3c5f1:      	vmovupd	%ymm1, -0x20(%rsp)
   3c5f7:      	vmovupd	0xe0(%rdi,%rax,8), %ymm8
   3c600:      	vmovddup	%ymm8, %ymm9            # ymm9 = ymm8[0,0,2,2]
   3c605:      	vshufpd	$0xf, %ymm8, %ymm8, %ymm8 # ymm8 = ymm8[1,1,3,3]
   3c60b:      	vsubpd	%ymm8, %ymm0, %ymm8
   3c610:      	vaddsubpd	%ymm8, %ymm9, %ymm8
   3c615:      	vpermpd	$0x44, %ymm8, %ymm9     # ymm9 = ymm8[0,1,0,1]
   3c61b:      	vsubpd	%ymm8, %ymm0, %ymm10
   3c620:      	vperm2f128	$0x31, %ymm10, %ymm8, %ymm8 # ymm8 = ymm8[2,3],ymm10[2,3]
   3c626:      	vaddpd	%ymm8, %ymm9, %ymm8
   3c62b:      	vmovupd	0x100(%rdi,%rax,8), %ymm9
   3c634:      	vmovddup	%ymm9, %ymm10           # ymm10 = ymm9[0,0,2,2]
   3c639:      	vshufpd	$0xf, %ymm9, %ymm9, %ymm9 # ymm9 = ymm9[1,1,3,3]
   3c63f:      	vsubpd	%ymm9, %ymm0, %ymm9
   3c644:      	vaddsubpd	%ymm9, %ymm10, %ymm9
   3c649:      	vpermpd	$0x44, %ymm9, %ymm10    # ymm10 = ymm9[0,1,0,1]
   3c64f:      	vsubpd	%ymm9, %ymm0, %ymm11
   3c654:      	vperm2f128	$0x31, %ymm11, %ymm9, %ymm9 # ymm9 = ymm9[2,3],ymm11[2,3]
   3c65a:      	vaddpd	%ymm9, %ymm10, %ymm9
   3c65f:      	vmovupd	0x120(%rdi,%rax,8), %ymm10
   3c668:      	vmovddup	%ymm10, %ymm11          # ymm11 = ymm10[0,0,2,2]
   3c66d:      	vshufpd	$0xf, %ymm10, %ymm10, %ymm10 # ymm10 = ymm10[1,1,3,3]
   3c673:      	vsubpd	%ymm10, %ymm0, %ymm10
   3c678:      	vaddsubpd	%ymm10, %ymm11, %ymm10
   3c67d:      	vpermpd	$0x44, %ymm10, %ymm11   # ymm11 = ymm10[0,1,0,1]
   3c683:      	vsubpd	%ymm10, %ymm0, %ymm12
   3c688:      	vperm2f128	$0x31, %ymm12, %ymm10, %ymm10 # ymm10 = ymm10[2,3],ymm12[2,3]
   3c68e:      	vaddpd	%ymm10, %ymm11, %ymm7
   3c693:      	vmovupd	0x140(%rdi,%rax,8), %ymm11
   3c69c:      	vmovddup	%ymm11, %ymm12          # ymm12 = ymm11[0,0,2,2]
   3c6a1:      	vshufpd	$0xf, %ymm11, %ymm11, %ymm11 # ymm11 = ymm11[1,1,3,3]
   3c6a7:      	vsubpd	%ymm11, %ymm0, %ymm11
   3c6ac:      	vaddsubpd	%ymm11, %ymm12, %ymm11
   3c6b1:      	vpermpd	$0x44, %ymm11, %ymm12   # ymm12 = ymm11[0,1,0,1]
   3c6b7:      	vsubpd	%ymm11, %ymm0, %ymm13
   3c6bc:      	vperm2f128	$0x31, %ymm13, %ymm11, %ymm11 # ymm11 = ymm11[2,3],ymm13[2,3]
   3c6c2:      	vaddpd	%ymm11, %ymm12, %ymm1
   3c6c7:      	vmovupd	%ymm1, (%rsp)
   3c6cc:      	vmovupd	0x160(%rdi,%rax,8), %ymm12
   3c6d5:      	vmovddup	%ymm12, %ymm13          # ymm13 = ymm12[0,0,2,2]
   3c6da:      	vshufpd	$0xf, %ymm12, %ymm12, %ymm12 # ymm12 = ymm12[1,1,3,3]
   3c6e0:      	vsubpd	%ymm12, %ymm0, %ymm12
   3c6e5:      	vaddsubpd	%ymm12, %ymm13, %ymm12
   3c6ea:      	vpermpd	$0x44, %ymm12, %ymm13   # ymm13 = ymm12[0,1,0,1]
   3c6f0:      	vsubpd	%ymm12, %ymm0, %ymm14
   3c6f5:      	vperm2f128	$0x31, %ymm14, %ymm12, %ymm12 # ymm12 = ymm12[2,3],ymm14[2,3]
   3c6fb:      	vaddpd	%ymm12, %ymm13, %ymm12
   3c700:      	vmovupd	0x180(%rdi,%rax,8), %ymm13
   3c709:      	vmovddup	%ymm13, %ymm14          # ymm14 = ymm13[0,0,2,2]
   3c70e:      	vshufpd	$0xf, %ymm13, %ymm13, %ymm13 # ymm13 = ymm13[1,1,3,3]
   3c714:      	vsubpd	%ymm13, %ymm0, %ymm13
   3c719:      	vxorpd	%xmm3, %xmm3, %xmm3
   3c71d:      	vaddsubpd	%ymm13, %ymm14, %ymm13
   3c722:      	vpermpd	$0x44, %ymm13, %ymm14   # ymm14 = ymm13[0,1,0,1]
   3c728:      	vsubpd	%ymm13, %ymm3, %ymm15
   3c72d:      	vperm2f128	$0x31, %ymm15, %ymm13, %ymm13 # ymm13 = ymm13[2,3],ymm15[2,3]
   3c733:      	vaddpd	%ymm13, %ymm14, %ymm0
   3c738:      	vmovupd	%ymm0, -0x40(%rsp)
   3c73e:      	vmovupd	0x1a0(%rdi,%rax,8), %ymm14
   3c747:      	vmovddup	%ymm14, %ymm15          # ymm15 = ymm14[0,0,2,2]
   3c74c:      	vshufpd	$0xf, %ymm14, %ymm14, %ymm14 # ymm14 = ymm14[1,1,3,3]
   3c752:      	vsubpd	%ymm14, %ymm3, %ymm14
   3c757:      	vaddsubpd	%ymm14, %ymm15, %ymm14
   3c75c:      	vpermpd	$0x44, %ymm14, %ymm15   # ymm15 = ymm14[0,1,0,1]
   3c762:      	vsubpd	%ymm14, %ymm3, %ymm1
   3c767:      	vperm2f128	$0x31, %ymm1, %ymm14, %ymm1 # ymm1 = ymm14[2,3],ymm1[2,3]
   3c76d:      	vaddpd	%ymm1, %ymm15, %ymm14
   3c771:      	vmovupd	0x1c0(%rdi,%rax,8), %ymm1
   3c77a:      	vmovddup	%ymm1, %ymm15           # ymm15 = ymm1[0,0,2,2]
   3c77e:      	vshufpd	$0xf, %ymm1, %ymm1, %ymm1 # ymm1 = ymm1[1,1,3,3]
   3c783:      	vsubpd	%ymm1, %ymm3, %ymm1
   3c787:      	vaddsubpd	%ymm1, %ymm15, %ymm1
   3c78b:      	vsubpd	%ymm1, %ymm3, %ymm15
   3c78f:      	vperm2f128	$0x31, %ymm15, %ymm1, %ymm15 # ymm15 = ymm1[2,3],ymm15[2,3]
   3c795:      	vpermpd	$0x44, %ymm1, %ymm1     # ymm1 = ymm1[0,1,0,1]
   3c79b:      	vaddpd	%ymm1, %ymm15, %ymm10
   3c79f:      	vmovupd	0x1e0(%rdi,%rax,8), %ymm15
   3c7a8:      	vmovddup	%ymm15, %ymm0           # ymm0 = ymm15[0,0,2,2]
   3c7ad:      	vshufpd	$0xf, %ymm15, %ymm15, %ymm15 # ymm15 = ymm15[1,1,3,3]
   3c7b3:      	vsubpd	%ymm15, %ymm3, %ymm15
   3c7b8:      	vaddsubpd	%ymm15, %ymm0, %ymm0
   3c7bd:      	vsubpd	%ymm0, %ymm3, %ymm15
   3c7c1:      	vperm2f128	$0x31, %ymm15, %ymm0, %ymm15 # ymm15 = ymm0[2,3],ymm15[2,3]
   3c7c7:      	vpermpd	$0x44, %ymm0, %ymm0     # ymm0 = ymm0[0,1,0,1]
   3c7cd:      	vaddpd	%ymm0, %ymm15, %ymm5
   3c7d1:      	vmovupd	-0x60(%rsp), %ymm0
   3c7d7:      	vmovupd	-0x80(%rsp), %ymm1
   3c7dd:      	vaddpd	%ymm1, %ymm0, %ymm15
   3c7e1:      	vsubpd	%ymm1, %ymm0, %ymm11
   3c7e5:      	vmovupd	0x40(%rsp), %ymm1
   3c7eb:      	vaddpd	%ymm4, %ymm1, %ymm0
   3c7ef:      	vsubpd	%ymm4, %ymm1, %ymm4
   3c7f3:      	vmovupd	0x20(%rsp), %ymm1
   3c7f9:      	vaddpd	%ymm2, %ymm1, %ymm6
   3c7fd:      	vsubpd	%ymm2, %ymm1, %ymm13
   3c801:      	vmovupd	-0x20(%rsp), %ymm2
   3c807:      	vaddpd	%ymm2, %ymm8, %ymm1
   3c80b:      	vsubpd	%ymm8, %ymm2, %ymm8
   3c810:      	vmovapd	%ymm9, %ymm2
   3c814:      	vaddpd	%ymm7, %ymm9, %ymm9
   3c818:      	vsubpd	%ymm7, %ymm2, %ymm2
   3c81c:      	vmovupd	%ymm2, -0x80(%rsp)
   3c822:      	vmovupd	(%rsp), %ymm3
   3c827:      	vaddpd	%ymm3, %ymm12, %ymm2
   3c82b:      	vsubpd	%ymm12, %ymm3, %ymm12
   3c830:      	vmovupd	-0x40(%rsp), %ymm3
   3c836:      	vaddpd	%ymm3, %ymm14, %ymm7
   3c83a:      	vsubpd	%ymm14, %ymm3, %ymm14
   3c83f:      	vaddpd	%ymm5, %ymm10, %ymm3
   3c843:      	vsubpd	%ymm5, %ymm10, %ymm5
   3c847:      	vaddpd	%ymm0, %ymm15, %ymm10
   3c84b:      	vsubpd	%ymm0, %ymm15, %ymm0
   3c84f:      	vaddpd	%ymm4, %ymm11, %ymm15
   3c853:      	vsubpd	%ymm4, %ymm11, %ymm4
   3c857:      	vaddpd	%ymm1, %ymm6, %ymm11
   3c85b:      	vsubpd	%ymm1, %ymm6, %ymm1
   3c85f:      	vaddpd	%ymm8, %ymm13, %ymm6
   3c864:      	vsubpd	%ymm8, %ymm13, %ymm8
   3c869:      	vaddpd	%ymm2, %ymm9, %ymm13
   3c86d:      	vsubpd	%ymm2, %ymm9, %ymm2
   3c871:      	vmovupd	%ymm2, -0x60(%rsp)
   3c877:      	vmovupd	-0x80(%rsp), %ymm2
   3c87d:      	vaddpd	%ymm2, %ymm12, %ymm9
   3c881:      	vsubpd	%ymm12, %ymm2, %ymm12
   3c886:      	vaddpd	%ymm3, %ymm7, %ymm2
   3c88a:      	vsubpd	%ymm3, %ymm7, %ymm3
   3c88e:      	vaddpd	%ymm5, %ymm14, %ymm7
   3c892:      	vsubpd	%ymm5, %ymm14, %ymm5
   3c896:      	vaddpd	%ymm11, %ymm10, %ymm14
   3c89b:      	vsubpd	%ymm11, %ymm10, %ymm10
   3c8a0:      	vaddpd	%ymm6, %ymm15, %ymm11
   3c8a4:      	vsubpd	%ymm6, %ymm15, %ymm6
   3c8a8:      	vaddpd	%ymm1, %ymm0, %ymm15
   3c8ac:      	vsubpd	%ymm1, %ymm0, %ymm1
   3c8b0:      	vmovupd	%ymm1, -0x80(%rsp)
   3c8b6:      	vaddpd	%ymm4, %ymm8, %ymm1
   3c8ba:      	vsubpd	%ymm8, %ymm4, %ymm4
   3c8bf:      	vaddpd	%ymm2, %ymm13, %ymm8
   3c8c3:      	vsubpd	%ymm2, %ymm13, %ymm0
   3c8c7:      	vaddpd	%ymm7, %ymm9, %ymm13
   3c8cb:      	vsubpd	%ymm7, %ymm9, %ymm7
   3c8cf:      	vmovupd	-0x60(%rsp), %ymm2
   3c8d5:      	vaddpd	%ymm3, %ymm2, %ymm9
   3c8d9:      	vsubpd	%ymm3, %ymm2, %ymm2
   3c8dd:      	vaddpd	%ymm5, %ymm12, %ymm3
   3c8e1:      	vsubpd	%ymm5, %ymm12, %ymm5
   3c8e5:      	vaddpd	%ymm8, %ymm14, %ymm12
   3c8ea:      	vsubpd	%ymm8, %ymm14, %ymm8
   3c8ef:      	vmovupd	%ymm8, -0x60(%rsp)
   3c8f5:      	vaddpd	%ymm13, %ymm11, %ymm14
   3c8fa:      	vsubpd	%ymm13, %ymm11, %ymm11
   3c8ff:      	vaddpd	%ymm9, %ymm15, %ymm13
   3c904:      	vsubpd	%ymm9, %ymm15, %ymm9
   3c909:      	vaddpd	%ymm3, %ymm1, %ymm15
   3c90d:      	vsubpd	%ymm3, %ymm1, %ymm8
   3c911:      	vaddpd	%ymm0, %ymm10, %ymm3
   3c915:      	vsubpd	%ymm0, %ymm10, %ymm1
   3c919:      	vaddpd	%ymm7, %ymm6, %ymm10
   3c91d:      	vsubpd	%ymm7, %ymm6, %ymm6
   3c921:      	vmovupd	-0x80(%rsp), %ymm0
   3c927:      	vaddpd	%ymm2, %ymm0, %ymm7
   3c92b:      	vsubpd	%ymm2, %ymm0, %ymm2
   3c92f:      	vaddpd	%ymm5, %ymm4, %ymm0
   3c933:      	vsubpd	%ymm5, %ymm4, %ymm4
   3c937:      	vmovupd	%ymm12, (%rdi,%rax,8)
   3c93c:      	vmovupd	%ymm14, 0x20(%rdi,%rax,8)
   3c942:      	vmovupd	%ymm13, 0x40(%rdi,%rax,8)
   3c948:      	vmovupd	%ymm15, 0x60(%rdi,%rax,8)
   3c94e:      	vmovupd	%ymm3, 0x80(%rdi,%rax,8)
   3c957:      	vmovupd	%ymm10, 0xa0(%rdi,%rax,8)
   3c960:      	vmovupd	%ymm7, 0xc0(%rdi,%rax,8)
   3c969:      	vmovupd	%ymm0, 0xe0(%rdi,%rax,8)
   3c972:      	vmovups	-0x60(%rsp), %ymm0
   3c978:      	vmovups	%ymm0, 0x100(%rdi,%rax,8)
   3c981:      	vmovupd	%ymm11, 0x120(%rdi,%rax,8)
   3c98a:      	vmovupd	%ymm9, 0x140(%rdi,%rax,8)
   3c993:      	vmovupd	%ymm8, 0x160(%rdi,%rax,8)
   3c99c:      	vmovupd	%ymm1, 0x180(%rdi,%rax,8)
   3c9a5:      	vmovupd	%ymm6, 0x1a0(%rdi,%rax,8)
   3c9ae:      	vmovupd	%ymm2, 0x1c0(%rdi,%rax,8)
   3c9b7:      	vmovupd	%ymm4, 0x1e0(%rdi,%rax,8)
   3c9c0:      	addq	$0x40, %rax
   3c9c4:      	cmpq	%rsi, %rax
   3c9c7:      	jb	0x3c4a0 <hfirst_tb16_nat+0x20>
   3c9cd:      	addq	$0x68, %rsp
   3c9d1:      	vzeroupper
   3c9d4:      	retq
   3c9d5:      	nopw	%cs:(%rax,%rax)

000000000003c9e0 <hstep_tb16_nat>:
   3c9e0:      	pushq	%rbp
   3c9e1:      	pushq	%r15
   3c9e3:      	pushq	%r14
   3c9e5:      	pushq	%r13
   3c9e7:      	pushq	%r12
   3c9e9:      	pushq	%rbx
   3c9ea:      	subq	$0x78, %rsp
   3c9ee:      	movq	%rdx, -0x70(%rsp)
   3c9f3:      	vmovaps	(%rip), %ymm0           # 0x3c9fb <hstep_tb16_nat+0x1b>
   3c9fb:      	movq	%rsi, 0x28(%rsp)
   3ca00:      	testq	%rsi, %rsi
   3ca03:      	je	0x3ce19 <hstep_tb16_nat+0x439>
   3ca09:      	cmpq	$0x0, -0x70(%rsp)
   3ca0f:      	je	0x3ce19 <hstep_tb16_nat+0x439>
   3ca15:      	movq	-0x70(%rsp), %rcx
   3ca1a:      	movq	%rcx, %rbx
   3ca1d:      	shlq	$0x4, %rbx
   3ca21:      	leaq	(%rcx,%rcx,2), %r10
   3ca25:      	movq	%rcx, %rax
   3ca28:      	shlq	$0x5, %rax
   3ca2c:      	movq	%rax, -0x78(%rsp)
   3ca31:      	leaq	(%rcx,%rcx,4), %r12
   3ca35:      	movq	%r10, %r9
   3ca38:      	leaq	(%rdi,%r10,8), %rax
   3ca3c:      	movq	%rax, -0x50(%rsp)
   3ca41:      	movq	%r10, %rax
   3ca44:      	shlq	$0x4, %rax
   3ca48:      	imulq	$0x38, %rcx, %r14
   3ca4c:      	movq	%rcx, %r10
   3ca4f:      	shlq	$0x6, %r10
   3ca53:      	leaq	(%rcx,%rcx,8), %rdx
   3ca57:      	leaq	(%rdi,%r12,8), %r13
   3ca5b:      	shlq	$0x4, %r12
   3ca5f:      	imulq	$0x58, %rcx, %rbp
   3ca63:      	shlq	$0x5, %r9
   3ca67:      	imulq	$0x68, %rcx, %rsi
   3ca6b:      	imulq	$0x70, %rcx, %r8
   3ca6f:      	imulq	$0x78, %rcx, %r11
   3ca73:      	addq	%rdi, %r11
   3ca76:      	movq	%r11, -0x40(%rsp)
   3ca7b:      	movq	%rcx, %r11
   3ca7e:      	shlq	$0x7, %r11
   3ca82:      	movq	%r11, 0x18(%rsp)
   3ca87:      	addq	%rdi, %r8
   3ca8a:      	movq	%r8, -0x48(%rsp)
   3ca8f:      	addq	%rdi, %rsi
   3ca92:      	movq	%rsi, -0x68(%rsp)
   3ca97:      	addq	%rdi, %r9
   3ca9a:      	movq	%r9, %r11
   3ca9d:      	addq	%rdi, %rbp
   3caa0:      	addq	%rdi, %r12
   3caa3:      	movq	%r12, %r15
   3caa6:      	leaq	(%rdi,%rdx,8), %r8
   3caaa:      	addq	%rdi, %r10
   3caad:      	movq	%r10, %r12
   3cab0:      	addq	%rdi, %r14
   3cab3:      	addq	%rdi, %rax
   3cab6:      	movq	%rax, %r10
   3cab9:      	movq	-0x78(%rsp), %r9
   3cabe:      	addq	%rdi, %r9
   3cac1:      	movq	%rbx, 0x20(%rsp)
   3cac6:      	leaq	(%rdi,%rbx), %rax
   3caca:      	leaq	(%rdi,%rcx,8), %rbx
   3cace:      	movq	$0x0, -0x58(%rsp)
   3cad7:      	nopw	(%rax,%rax)
   3cae0:      	movq	%rbp, -0x38(%rsp)
   3cae5:      	movq	%r11, -0x60(%rsp)
   3caea:      	movq	%r15, -0x30(%rsp)
   3caef:      	movq	%r8, -0x28(%rsp)
   3caf4:      	movq	%r12, -0x20(%rsp)
   3caf9:      	movq	%r14, -0x18(%rsp)
   3cafe:      	movq	%r10, -0x10(%rsp)
   3cb03:      	movq	%r13, -0x8(%rsp)
   3cb08:      	movq	%rax, (%rsp)
   3cb0c:      	movq	%r9, -0x78(%rsp)
   3cb11:      	movq	%rbx, 0x8(%rsp)
   3cb16:      	movq	%rdi, 0x10(%rsp)
   3cb1b:      	xorl	%edi, %edi
   3cb1d:      	nopl	(%rax)
   3cb20:      	movq	0x10(%rsp), %rsi
   3cb25:      	vmovupd	(%rsi,%rdi,8), %ymm0
   3cb2a:      	movq	0x8(%rsp), %rcx
   3cb2f:      	vmovupd	(%rcx,%rdi,8), %ymm1
   3cb34:      	movq	(%rsp), %r13
   3cb38:      	vmovupd	(%r13,%rdi,8), %ymm2
   3cb3f:      	movq	-0x50(%rsp), %r9
   3cb44:      	vmovupd	(%r9,%rdi,8), %ymm3
   3cb4a:      	movq	-0x78(%rsp), %r8
   3cb4f:      	vmovupd	(%r8,%rdi,8), %ymm4
   3cb55:      	movq	-0x8(%rsp), %r10
   3cb5a:      	vmovupd	(%r10,%rdi,8), %ymm5
   3cb60:      	movq	-0x10(%rsp), %r14
   3cb65:      	vmovupd	(%r14,%rdi,8), %ymm6
   3cb6b:      	movq	-0x18(%rsp), %r12
   3cb70:      	vmovupd	(%r12,%rdi,8), %ymm7
   3cb76:      	movq	-0x20(%rsp), %rdx
   3cb7b:      	vmovupd	(%rdx,%rdi,8), %ymm8
   3cb80:      	movq	-0x28(%rsp), %r15
   3cb85:      	vmovupd	(%r15,%rdi,8), %ymm9
   3cb8b:      	movq	-0x30(%rsp), %r11
   3cb90:      	vmovupd	(%r11,%rdi,8), %ymm10
   3cb96:      	movq	-0x38(%rsp), %rbx
   3cb9b:      	vmovupd	(%rbx,%rdi,8), %ymm11
   3cba0:      	movq	-0x60(%rsp), %rax
   3cba5:      	vmovupd	(%rax,%rdi,8), %ymm12
   3cbaa:      	movq	-0x68(%rsp), %rax
   3cbaf:      	vmovupd	(%rax,%rdi,8), %ymm13
   3cbb4:      	movq	-0x48(%rsp), %rbp
   3cbb9:      	vmovupd	(%rbp,%rdi,8), %ymm14
   3cbbf:      	vaddpd	%ymm1, %ymm0, %ymm15
   3cbc3:      	vsubpd	%ymm1, %ymm0, %ymm0
   3cbc7:      	vmovupd	%ymm0, 0x30(%rsp)
   3cbcd:      	vaddpd	%ymm3, %ymm2, %ymm0
   3cbd1:      	vsubpd	%ymm3, %ymm2, %ymm2
   3cbd5:      	vaddpd	%ymm5, %ymm4, %ymm3
   3cbd9:      	vsubpd	%ymm5, %ymm4, %ymm4
   3cbdd:      	vaddpd	%ymm7, %ymm6, %ymm5
   3cbe1:      	vsubpd	%ymm7, %ymm6, %ymm6
   3cbe5:      	vaddpd	%ymm9, %ymm8, %ymm7
   3cbea:      	vsubpd	%ymm9, %ymm8, %ymm8
   3cbef:      	vaddpd	%ymm11, %ymm10, %ymm9
   3cbf4:      	vsubpd	%ymm11, %ymm10, %ymm10
   3cbf9:      	vaddpd	%ymm13, %ymm12, %ymm11
   3cbfe:      	vsubpd	%ymm13, %ymm12, %ymm12
   3cc03:      	movq	-0x40(%rsp), %rax
   3cc08:      	vmovupd	(%rax,%rdi,8), %ymm13
   3cc0d:      	vaddpd	%ymm13, %ymm14, %ymm1
   3cc12:      	vsubpd	%ymm13, %ymm14, %ymm13
   3cc17:      	vaddpd	%ymm0, %ymm15, %ymm14
   3cc1b:      	vsubpd	%ymm0, %ymm15, %ymm0
   3cc1f:      	vmovupd	%ymm0, 0x50(%rsp)
   3cc25:      	vmovupd	0x30(%rsp), %ymm0
   3cc2b:      	vaddpd	%ymm2, %ymm0, %ymm15
   3cc2f:      	vsubpd	%ymm2, %ymm0, %ymm2
   3cc33:      	vaddpd	%ymm5, %ymm3, %ymm0
   3cc37:      	vsubpd	%ymm5, %ymm3, %ymm3
   3cc3b:      	vaddpd	%ymm6, %ymm4, %ymm5
   3cc3f:      	vsubpd	%ymm6, %ymm4, %ymm4
   3cc43:      	vaddpd	%ymm7, %ymm9, %ymm6
   3cc47:      	vsubpd	%ymm9, %ymm7, %ymm7
   3cc4c:      	vaddpd	%ymm10, %ymm8, %ymm9
   3cc51:      	vsubpd	%ymm10, %ymm8, %ymm8
   3cc56:      	vaddpd	%ymm1, %ymm11, %ymm10
   3cc5a:      	vsubpd	%ymm1, %ymm11, %ymm1
   3cc5e:      	vaddpd	%ymm13, %ymm12, %ymm11
   3cc63:      	vsubpd	%ymm13, %ymm12, %ymm12
   3cc68:      	vaddpd	%ymm0, %ymm14, %ymm13
   3cc6c:      	vsubpd	%ymm0, %ymm14, %ymm0
   3cc70:      	vmovupd	%ymm0, 0x30(%rsp)
   3cc76:      	vaddpd	%ymm5, %ymm15, %ymm14
   3cc7a:      	vsubpd	%ymm5, %ymm15, %ymm5
   3cc7e:      	vmovupd	0x50(%rsp), %ymm0
   3cc84:      	vaddpd	%ymm3, %ymm0, %ymm15
   3cc88:      	vsubpd	%ymm3, %ymm0, %ymm3
   3cc8c:      	vaddpd	%ymm4, %ymm2, %ymm0
   3cc90:      	vsubpd	%ymm4, %ymm2, %ymm2
   3cc94:      	vaddpd	%ymm6, %ymm10, %ymm4
   3cc98:      	vsubpd	%ymm10, %ymm6, %ymm6
   3cc9d:      	vaddpd	%ymm11, %ymm9, %ymm10
   3cca2:      	vsubpd	%ymm11, %ymm9, %ymm9
   3cca7:      	vaddpd	%ymm1, %ymm7, %ymm11
   3ccab:      	vsubpd	%ymm1, %ymm7, %ymm1
   3ccaf:      	vaddpd	%ymm12, %ymm8, %ymm7
   3ccb4:      	vsubpd	%ymm12, %ymm8, %ymm8
   3ccb9:      	vaddpd	%ymm4, %ymm13, %ymm12
   3ccbd:      	vsubpd	%ymm4, %ymm13, %ymm4
   3ccc1:      	vmovupd	%ymm4, 0x50(%rsp)
   3ccc7:      	vaddpd	%ymm10, %ymm14, %ymm13
   3cccc:      	vsubpd	%ymm10, %ymm14, %ymm10
   3ccd1:      	vaddpd	%ymm11, %ymm15, %ymm14
   3ccd6:      	vsubpd	%ymm11, %ymm15, %ymm11
   3ccdb:      	vaddpd	%ymm7, %ymm0, %ymm15
   3ccdf:      	vsubpd	%ymm7, %ymm0, %ymm4
   3cce3:      	vmovupd	0x30(%rsp), %ymm0
   3cce9:      	vaddpd	%ymm6, %ymm0, %ymm7
   3cced:      	vsubpd	%ymm6, %ymm0, %ymm6
   3ccf1:      	vaddpd	%ymm5, %ymm9, %ymm0
   3ccf5:      	vsubpd	%ymm9, %ymm5, %ymm5
   3ccfa:      	vaddpd	%ymm1, %ymm3, %ymm9
   3ccfe:      	vsubpd	%ymm1, %ymm3, %ymm1
   3cd02:      	vaddpd	%ymm2, %ymm8, %ymm3
   3cd06:      	vsubpd	%ymm8, %ymm2, %ymm2
   3cd0b:      	vmovupd	%ymm12, (%rsi,%rdi,8)
   3cd10:      	vmovupd	%ymm13, (%rcx,%rdi,8)
   3cd15:      	vmovupd	%ymm14, (%r13,%rdi,8)
   3cd1c:      	vmovupd	%ymm15, (%r9,%rdi,8)
   3cd22:      	vmovupd	%ymm7, (%r8,%rdi,8)
   3cd28:      	vmovupd	%ymm0, (%r10,%rdi,8)
   3cd2e:      	vmovupd	%ymm9, (%r14,%rdi,8)
   3cd34:      	vmovupd	%ymm3, (%r12,%rdi,8)
   3cd3a:      	vmovups	0x50(%rsp), %ymm0
   3cd40:      	vmovups	%ymm0, (%rdx,%rdi,8)
   3cd45:      	vmovupd	%ymm10, (%r15,%rdi,8)
   3cd4b:      	vmovupd	%ymm11, (%r11,%rdi,8)
   3cd51:      	vmovupd	%ymm4, (%rbx,%rdi,8)
   3cd56:      	movq	-0x60(%rsp), %rcx
   3cd5b:      	vmovupd	%ymm6, (%rcx,%rdi,8)
   3cd60:      	movq	-0x68(%rsp), %rcx
   3cd65:      	vmovupd	%ymm5, (%rcx,%rdi,8)
   3cd6a:      	vmovupd	%ymm1, (%rbp,%rdi,8)
   3cd70:      	vmovupd	%ymm2, (%rax,%rdi,8)
   3cd75:      	addq	$0x4, %rdi
   3cd79:      	cmpq	-0x70(%rsp), %rdi
   3cd7e:      	jb	0x3cb20 <hstep_tb16_nat+0x140>
   3cd84:      	movq	-0x58(%rsp), %rdx
   3cd89:      	addq	0x20(%rsp), %rdx
   3cd8e:      	movq	0x18(%rsp), %rdi
   3cd93:      	addq	%rdi, -0x40(%rsp)
   3cd98:      	addq	%rdi, -0x48(%rsp)
   3cd9d:      	addq	%rdi, -0x68(%rsp)
   3cda2:      	movq	-0x60(%rsp), %r11
   3cda7:      	addq	%rdi, %r11
   3cdaa:      	movq	-0x38(%rsp), %rbp
   3cdaf:      	addq	%rdi, %rbp
   3cdb2:      	movq	-0x30(%rsp), %r15
   3cdb7:      	addq	%rdi, %r15
   3cdba:      	movq	-0x28(%rsp), %r8
   3cdbf:      	addq	%rdi, %r8
   3cdc2:      	movq	-0x20(%rsp), %r12
   3cdc7:      	addq	%rdi, %r12
   3cdca:      	movq	-0x18(%rsp), %r14
   3cdcf:      	addq	%rdi, %r14
   3cdd2:      	movq	-0x10(%rsp), %r10
   3cdd7:      	addq	%rdi, %r10
   3cdda:      	movq	-0x8(%rsp), %r13
   3cddf:      	addq	%rdi, %r13
   3cde2:      	movq	-0x78(%rsp), %r9
   3cde7:      	addq	%rdi, %r9
   3cdea:      	addq	%rdi, -0x50(%rsp)
   3cdef:      	movq	(%rsp), %rax
   3cdf3:      	addq	%rdi, %rax
   3cdf6:      	movq	0x10(%rsp), %rsi
   3cdfb:      	addq	%rdi, %rsi
   3cdfe:      	movq	0x8(%rsp), %rbx
   3ce03:      	addq	%rdi, %rbx
   3ce06:      	movq	%rdx, -0x58(%rsp)
   3ce0b:      	cmpq	0x28(%rsp), %rdx
   3ce10:      	movq	%rsi, %rdi
   3ce13:      	jb	0x3cae0 <hstep_tb16_nat+0x100>
   3ce19:      	addq	$0x78, %rsp
   3ce1d:      	popq	%rbx
   3ce1e:      	popq	%r12
   3ce20:      	popq	%r13
   3ce22:      	popq	%r14
   3ce24:      	popq	%r15
   3ce26:      	popq	%rbp
   3ce27:      	vzeroupper
   3ce2a:      	retq
   3ce2b:      	nopl	(%rax,%rax)

000000000003ce30 <hfirst_g19_nat>:
   3ce30:      	vmovaps	(%rip), %ymm0           # 0x3ce38 <hfirst_g19_nat+0x8>
   3ce38:      	testq	%rsi, %rsi
   3ce3b:      	je	0x3d060 <hfirst_g19_nat+0x230>
   3ce41:      	xorl	%eax, %eax
   3ce43:      	vxorpd	%xmm0, %xmm0, %xmm0
   3ce47:      	vbroadcastsd	(%rip), %ymm1   # 0x3ce50 <hfirst_g19_nat+0x20>
   3ce50:      	vmovupd	(%rdi,%rax,8), %ymm2
   3ce55:      	vmovupd	0x20(%rdi,%rax,8), %ymm4
   3ce5b:      	vmovupd	0x40(%rdi,%rax,8), %ymm5
   3ce61:      	vmovupd	0x60(%rdi,%rax,8), %ymm6
   3ce67:      	vmovddup	%ymm2, %ymm3            # ymm3 = ymm2[0,0,2,2]
   3ce6b:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3ce70:      	vsubpd	%ymm2, %ymm0, %ymm2
   3ce74:      	vaddsubpd	%ymm2, %ymm3, %ymm2
   3ce78:      	vpermpd	$0x44, %ymm2, %ymm3     # ymm3 = ymm2[0,1,0,1]
   3ce7e:      	vsubpd	%ymm2, %ymm0, %ymm7
   3ce82:      	vperm2f128	$0x31, %ymm7, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm7[2,3]
   3ce88:      	vaddpd	%ymm2, %ymm3, %ymm3
   3ce8c:      	vmovddup	%ymm4, %ymm2            # ymm2 = ymm4[0,0,2,2]
   3ce90:      	vshufpd	$0xf, %ymm4, %ymm4, %ymm4 # ymm4 = ymm4[1,1,3,3]
   3ce95:      	vsubpd	%ymm4, %ymm0, %ymm4
   3ce99:      	vaddsubpd	%ymm4, %ymm2, %ymm2
   3ce9d:      	vpermpd	$0x44, %ymm2, %ymm4     # ymm4 = ymm2[0,1,0,1]
   3cea3:      	vsubpd	%ymm2, %ymm0, %ymm7
   3cea7:      	vperm2f128	$0x31, %ymm7, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm7[2,3]
   3cead:      	vaddpd	%ymm2, %ymm4, %ymm2
   3ceb1:      	vmovddup	%ymm5, %ymm4            # ymm4 = ymm5[0,0,2,2]
   3ceb5:      	vshufpd	$0xf, %ymm5, %ymm5, %ymm5 # ymm5 = ymm5[1,1,3,3]
   3ceba:      	vsubpd	%ymm5, %ymm0, %ymm5
   3cebe:      	vaddsubpd	%ymm5, %ymm4, %ymm4
   3cec2:      	vpermpd	$0x44, %ymm4, %ymm5     # ymm5 = ymm4[0,1,0,1]
   3cec8:      	vsubpd	%ymm4, %ymm0, %ymm7
   3cecc:      	vperm2f128	$0x31, %ymm7, %ymm4, %ymm4 # ymm4 = ymm4[2,3],ymm7[2,3]
   3ced2:      	vaddpd	%ymm4, %ymm5, %ymm7
   3ced6:      	vmovddup	%ymm6, %ymm4            # ymm4 = ymm6[0,0,2,2]
   3ceda:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm5 # ymm5 = ymm6[1,1,3,3]
   3cedf:      	vsubpd	%ymm5, %ymm0, %ymm5
   3cee3:      	vaddsubpd	%ymm5, %ymm4, %ymm4
   3cee7:      	vpermpd	$0x44, %ymm4, %ymm5     # ymm5 = ymm4[0,1,0,1]
   3ceed:      	vsubpd	%ymm4, %ymm0, %ymm6
   3cef1:      	vperm2f128	$0x31, %ymm6, %ymm4, %ymm4 # ymm4 = ymm4[2,3],ymm6[2,3]
   3cef7:      	vaddpd	%ymm4, %ymm5, %ymm5
   3cefb:      	vmovupd	0x80(%rdi,%rax,8), %ymm4
   3cf04:      	vmovddup	%ymm4, %ymm6            # ymm6 = ymm4[0,0,2,2]
   3cf08:      	vshufpd	$0xf, %ymm4, %ymm4, %ymm4 # ymm4 = ymm4[1,1,3,3]
   3cf0d:      	vsubpd	%ymm4, %ymm0, %ymm4
   3cf11:      	vaddsubpd	%ymm4, %ymm6, %ymm4
   3cf15:      	vpermpd	$0x44, %ymm4, %ymm6     # ymm6 = ymm4[0,1,0,1]
   3cf1b:      	vsubpd	%ymm4, %ymm0, %ymm8
   3cf1f:      	vperm2f128	$0x31, %ymm8, %ymm4, %ymm4 # ymm4 = ymm4[2,3],ymm8[2,3]
   3cf25:      	vaddpd	%ymm4, %ymm6, %ymm4
   3cf29:      	vmovupd	0xa0(%rdi,%rax,8), %ymm6
   3cf32:      	vmovddup	%ymm6, %ymm8            # ymm8 = ymm6[0,0,2,2]
   3cf36:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm6 # ymm6 = ymm6[1,1,3,3]
   3cf3b:      	vsubpd	%ymm6, %ymm0, %ymm6
   3cf3f:      	vaddsubpd	%ymm6, %ymm8, %ymm6
   3cf43:      	vpermpd	$0x44, %ymm6, %ymm8     # ymm8 = ymm6[0,1,0,1]
   3cf49:      	vsubpd	%ymm6, %ymm0, %ymm9
   3cf4d:      	vperm2f128	$0x31, %ymm9, %ymm6, %ymm6 # ymm6 = ymm6[2,3],ymm9[2,3]
   3cf53:      	vaddpd	%ymm6, %ymm8, %ymm6
   3cf57:      	vmovupd	0xc0(%rdi,%rax,8), %ymm8
   3cf60:      	vmovddup	%ymm8, %ymm9            # ymm9 = ymm8[0,0,2,2]
   3cf65:      	vshufpd	$0xf, %ymm8, %ymm8, %ymm8 # ymm8 = ymm8[1,1,3,3]
   3cf6b:      	vsubpd	%ymm8, %ymm0, %ymm8
   3cf70:      	vaddsubpd	%ymm8, %ymm9, %ymm8
   3cf75:      	vpermpd	$0x44, %ymm8, %ymm9     # ymm9 = ymm8[0,1,0,1]
   3cf7b:      	vsubpd	%ymm8, %ymm0, %ymm10
   3cf80:      	vperm2f128	$0x31, %ymm10, %ymm8, %ymm8 # ymm8 = ymm8[2,3],ymm10[2,3]
   3cf86:      	vaddpd	%ymm8, %ymm9, %ymm8
   3cf8b:      	vmovupd	0xe0(%rdi,%rax,8), %ymm9
   3cf94:      	vmovddup	%ymm9, %ymm10           # ymm10 = ymm9[0,0,2,2]
   3cf99:      	vshufpd	$0xf, %ymm9, %ymm9, %ymm9 # ymm9 = ymm9[1,1,3,3]
   3cf9f:      	vsubpd	%ymm9, %ymm0, %ymm9
   3cfa4:      	vaddsubpd	%ymm9, %ymm10, %ymm9
   3cfa9:      	vpermpd	$0x44, %ymm9, %ymm10    # ymm10 = ymm9[0,1,0,1]
   3cfaf:      	vsubpd	%ymm9, %ymm0, %ymm11
   3cfb4:      	vperm2f128	$0x31, %ymm11, %ymm9, %ymm9 # ymm9 = ymm9[2,3],ymm11[2,3]
   3cfba:      	vaddpd	%ymm9, %ymm10, %ymm9
   3cfbf:      	vaddpd	%ymm3, %ymm9, %ymm10
   3cfc3:      	vaddpd	%ymm2, %ymm8, %ymm3
   3cfc7:      	vsubpd	%ymm6, %ymm7, %ymm11
   3cfcb:      	vsubpd	%ymm4, %ymm5, %ymm7
   3cfcf:      	vsubpd	%ymm3, %ymm10, %ymm12
   3cfd3:      	vaddpd	%ymm7, %ymm11, %ymm13
   3cfd7:      	vsubpd	%ymm13, %ymm12, %ymm14
   3cfdc:      	vfnmadd213pd	%ymm14, %ymm1, %ymm9 # ymm9 = -(ymm1 * ymm9) + ymm14
   3cfe1:      	vfnmadd213pd	%ymm14, %ymm1, %ymm6 # ymm6 = -(ymm1 * ymm6) + ymm14
   3cfe6:      	vfmadd213pd	%ymm9, %ymm1, %ymm8 # ymm8 = (ymm1 * ymm8) + ymm9
   3cfeb:      	vfnmadd213pd	%ymm6, %ymm1, %ymm4 # ymm4 = -(ymm1 * ymm4) + ymm6
   3cff0:      	vfmadd213pd	%ymm8, %ymm1, %ymm7 # ymm7 = (ymm1 * ymm7) + ymm8
   3cff5:      	vfmadd231pd	%ymm5, %ymm1, %ymm6 # ymm6 = (ymm1 * ymm5) + ymm6
   3cffa:      	vfmsub213pd	%ymm6, %ymm1, %ymm12 # ymm12 = (ymm1 * ymm12) - ymm6
   3cfff:      	vfmadd231pd	%ymm11, %ymm1, %ymm8 # ymm8 = (ymm1 * ymm11) + ymm8
   3d004:      	vfmadd213pd	%ymm4, %ymm1, %ymm3 # ymm3 = (ymm1 * ymm3) + ymm4
   3d009:      	vfmadd231pd	%ymm2, %ymm1, %ymm9 # ymm9 = (ymm1 * ymm2) + ymm9
   3d00e:      	vfmadd213pd	%ymm9, %ymm1, %ymm13 # ymm13 = (ymm1 * ymm13) + ymm9
   3d013:      	vfmsub231pd	%ymm10, %ymm1, %ymm4 # ymm4 = (ymm1 * ymm10) - ymm4
   3d018:      	vmovupd	%ymm4, (%rdi,%rax,8)
   3d01d:      	vmovupd	%ymm8, 0x20(%rdi,%rax,8)
   3d023:      	vmovupd	%ymm9, 0x40(%rdi,%rax,8)
   3d029:      	vmovupd	%ymm6, 0x60(%rdi,%rax,8)
   3d02f:      	vmovupd	%ymm13, 0x80(%rdi,%rax,8)
   3d038:      	vmovupd	%ymm12, 0xa0(%rdi,%rax,8)
   3d041:      	vmovupd	%ymm3, 0xc0(%rdi,%rax,8)
   3d04a:      	vmovupd	%ymm7, 0xe0(%rdi,%rax,8)
   3d053:      	addq	$0x20, %rax
   3d057:      	cmpq	%rsi, %rax
   3d05a:      	jb	0x3ce50 <hfirst_g19_nat+0x20>
   3d060:      	vzeroupper
   3d063:      	retq
   3d064:      	nopw	%cs:(%rax,%rax)

000000000003d070 <hstep_g19_nat>:
   3d070:      	pushq	%r15
   3d072:      	pushq	%r14
   3d074:      	pushq	%r13
   3d076:      	pushq	%r12
   3d078:      	pushq	%rbx
   3d079:      	vmovaps	(%rip), %ymm0           # 0x3d081 <hstep_g19_nat+0x11>
   3d081:      	testq	%rsi, %rsi
   3d084:      	je	0x3d1e6 <hstep_g19_nat+0x176>
   3d08a:      	testq	%rdx, %rdx
   3d08d:      	je	0x3d1e6 <hstep_g19_nat+0x176>
   3d093:      	leaq	(,%rdx,8), %rax
   3d09b:      	movq	%rdx, %rcx
   3d09e:      	shlq	$0x4, %rcx
   3d0a2:      	leaq	(%rdx,%rdx,2), %r8
   3d0a6:      	movq	%rdx, %r9
   3d0a9:      	shlq	$0x5, %r9
   3d0ad:      	leaq	(%rdx,%rdx,4), %r14
   3d0b1:      	leaq	(%rdi,%r8,8), %r10
   3d0b5:      	shlq	$0x4, %r8
   3d0b9:      	imulq	$0x38, %rdx, %r11
   3d0bd:      	addq	%rdi, %r11
   3d0c0:      	movq	%rdx, %rbx
   3d0c3:      	shlq	$0x6, %rbx
   3d0c7:      	addq	%rdi, %r8
   3d0ca:      	leaq	(%rdi,%r14,8), %r14
   3d0ce:      	addq	%rdi, %r9
   3d0d1:      	addq	%rdi, %rcx
   3d0d4:      	leaq	(%rdi,%rax), %r15
   3d0d8:      	xorl	%r12d, %r12d
   3d0db:      	vbroadcastsd	(%rip), %ymm0   # 0x3d0e4 <hstep_g19_nat+0x74>
   3d0e4:      	nopw	%cs:(%rax,%rax)
   3d0f0:      	xorl	%r13d, %r13d
   3d0f3:      	nopw	%cs:(%rax,%rax)
   3d100:      	vmovupd	(%r15,%r13,8), %ymm7
   3d106:      	vmovupd	(%rcx,%r13,8), %ymm3
   3d10c:      	vmovupd	(%r10,%r13,8), %ymm8
   3d112:      	vmovupd	(%r9,%r13,8), %ymm4
   3d118:      	vmovupd	(%r14,%r13,8), %ymm1
   3d11e:      	vmovupd	(%r8,%r13,8), %ymm5
   3d124:      	vmovupd	(%r11,%r13,8), %ymm6
   3d12a:      	vaddpd	(%rdi,%r13,8), %ymm6, %ymm9
   3d130:      	vaddpd	%ymm5, %ymm7, %ymm2
   3d134:      	vsubpd	%ymm1, %ymm3, %ymm10
   3d138:      	vsubpd	%ymm4, %ymm8, %ymm3
   3d13c:      	vsubpd	%ymm2, %ymm9, %ymm11
   3d140:      	vaddpd	%ymm3, %ymm10, %ymm12
   3d144:      	vsubpd	%ymm12, %ymm11, %ymm13
   3d149:      	vfnmadd213pd	%ymm13, %ymm0, %ymm6 # ymm6 = -(ymm0 * ymm6) + ymm13
   3d14e:      	vfnmadd213pd	%ymm13, %ymm0, %ymm1 # ymm1 = -(ymm0 * ymm1) + ymm13
   3d153:      	vfmadd213pd	%ymm6, %ymm0, %ymm5 # ymm5 = (ymm0 * ymm5) + ymm6
   3d158:      	vfnmadd213pd	%ymm1, %ymm0, %ymm4 # ymm4 = -(ymm0 * ymm4) + ymm1
   3d15d:      	vfmadd213pd	%ymm5, %ymm0, %ymm3 # ymm3 = (ymm0 * ymm3) + ymm5
   3d162:      	vfmadd231pd	%ymm8, %ymm0, %ymm1 # ymm1 = (ymm0 * ymm8) + ymm1
   3d167:      	vfmsub213pd	%ymm1, %ymm0, %ymm11 # ymm11 = (ymm0 * ymm11) - ymm1
   3d16c:      	vfmadd231pd	%ymm10, %ymm0, %ymm5 # ymm5 = (ymm0 * ymm10) + ymm5
   3d171:      	vfmadd213pd	%ymm4, %ymm0, %ymm2 # ymm2 = (ymm0 * ymm2) + ymm4
   3d176:      	vfmadd231pd	%ymm7, %ymm0, %ymm6 # ymm6 = (ymm0 * ymm7) + ymm6
   3d17b:      	vfmadd213pd	%ymm6, %ymm0, %ymm12 # ymm12 = (ymm0 * ymm12) + ymm6
   3d180:      	vfmsub231pd	%ymm9, %ymm0, %ymm4 # ymm4 = (ymm0 * ymm9) - ymm4
   3d185:      	vmovupd	%ymm4, (%rdi,%r13,8)
   3d18b:      	vmovupd	%ymm5, (%r15,%r13,8)
   3d191:      	vmovupd	%ymm6, (%rcx,%r13,8)
   3d197:      	vmovupd	%ymm1, (%r10,%r13,8)
   3d19d:      	vmovupd	%ymm12, (%r9,%r13,8)
   3d1a3:      	vmovupd	%ymm11, (%r14,%r13,8)
   3d1a9:      	vmovupd	%ymm2, (%r8,%r13,8)
   3d1af:      	vmovupd	%ymm3, (%r11,%r13,8)
   3d1b5:      	addq	$0x4, %r13
   3d1b9:      	cmpq	%rdx, %r13
   3d1bc:      	jb	0x3d100 <hstep_g19_nat+0x90>
   3d1c2:      	addq	%rax, %r12
   3d1c5:      	addq	%rbx, %r11
   3d1c8:      	addq	%rbx, %r8
   3d1cb:      	addq	%rbx, %r14
   3d1ce:      	addq	%rbx, %r9
   3d1d1:      	addq	%rbx, %r10
   3d1d4:      	addq	%rbx, %rcx
   3d1d7:      	addq	%rbx, %rdi
   3d1da:      	addq	%rbx, %r15
   3d1dd:      	cmpq	%rsi, %r12
   3d1e0:      	jb	0x3d0f0 <hstep_g19_nat+0x80>
   3d1e6:      	popq	%rbx
   3d1e7:      	popq	%r12
   3d1e9:      	popq	%r13
   3d1eb:      	popq	%r14
   3d1ed:      	popq	%r15
   3d1ef:      	vzeroupper
   3d1f2:      	retq
   3d1f3:      	nopw	%cs:(%rax,%rax)

000000000003d200 <hfirst_g20_nat>:
   3d200:      	vmovaps	(%rip), %ymm0           # 0x3d208 <hfirst_g20_nat+0x8>
   3d208:      	testq	%rsi, %rsi
   3d20b:      	je	0x3d42f <hfirst_g20_nat+0x22f>
   3d211:      	xorl	%eax, %eax
   3d213:      	vxorpd	%xmm0, %xmm0, %xmm0
   3d217:      	vbroadcastsd	(%rip), %ymm1   # 0x3d220 <hfirst_g20_nat+0x20>
   3d220:      	vmovupd	(%rdi,%rax,8), %ymm2
   3d225:      	vmovupd	0x20(%rdi,%rax,8), %ymm3
   3d22b:      	vmovupd	0x40(%rdi,%rax,8), %ymm4
   3d231:      	vmovupd	0x60(%rdi,%rax,8), %ymm6
   3d237:      	vmovddup	%ymm2, %ymm5            # ymm5 = ymm2[0,0,2,2]
   3d23b:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3d240:      	vsubpd	%ymm2, %ymm0, %ymm2
   3d244:      	vaddsubpd	%ymm2, %ymm5, %ymm2
   3d248:      	vpermpd	$0x44, %ymm2, %ymm5     # ymm5 = ymm2[0,1,0,1]
   3d24e:      	vsubpd	%ymm2, %ymm0, %ymm7
   3d252:      	vperm2f128	$0x31, %ymm7, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm7[2,3]
   3d258:      	vaddpd	%ymm2, %ymm5, %ymm2
   3d25c:      	vmovddup	%ymm3, %ymm5            # ymm5 = ymm3[0,0,2,2]
   3d260:      	vshufpd	$0xf, %ymm3, %ymm3, %ymm3 # ymm3 = ymm3[1,1,3,3]
   3d265:      	vsubpd	%ymm3, %ymm0, %ymm3
   3d269:      	vaddsubpd	%ymm3, %ymm5, %ymm3
   3d26d:      	vpermpd	$0x44, %ymm3, %ymm5     # ymm5 = ymm3[0,1,0,1]
   3d273:      	vsubpd	%ymm3, %ymm0, %ymm7
   3d277:      	vperm2f128	$0x31, %ymm7, %ymm3, %ymm3 # ymm3 = ymm3[2,3],ymm7[2,3]
   3d27d:      	vaddpd	%ymm3, %ymm5, %ymm5
   3d281:      	vmovddup	%ymm4, %ymm3            # ymm3 = ymm4[0,0,2,2]
   3d285:      	vshufpd	$0xf, %ymm4, %ymm4, %ymm4 # ymm4 = ymm4[1,1,3,3]
   3d28a:      	vsubpd	%ymm4, %ymm0, %ymm4
   3d28e:      	vaddsubpd	%ymm4, %ymm3, %ymm3
   3d292:      	vpermpd	$0x44, %ymm3, %ymm4     # ymm4 = ymm3[0,1,0,1]
   3d298:      	vsubpd	%ymm3, %ymm0, %ymm7
   3d29c:      	vperm2f128	$0x31, %ymm7, %ymm3, %ymm3 # ymm3 = ymm3[2,3],ymm7[2,3]
   3d2a2:      	vaddpd	%ymm3, %ymm4, %ymm3
   3d2a6:      	vmovddup	%ymm6, %ymm4            # ymm4 = ymm6[0,0,2,2]
   3d2aa:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm6 # ymm6 = ymm6[1,1,3,3]
   3d2af:      	vsubpd	%ymm6, %ymm0, %ymm6
   3d2b3:      	vaddsubpd	%ymm6, %ymm4, %ymm4
   3d2b7:      	vpermpd	$0x44, %ymm4, %ymm6     # ymm6 = ymm4[0,1,0,1]
   3d2bd:      	vsubpd	%ymm4, %ymm0, %ymm7
   3d2c1:      	vperm2f128	$0x31, %ymm7, %ymm4, %ymm4 # ymm4 = ymm4[2,3],ymm7[2,3]
   3d2c7:      	vaddpd	%ymm4, %ymm6, %ymm7
   3d2cb:      	vmovupd	0x80(%rdi,%rax,8), %ymm4
   3d2d4:      	vmovddup	%ymm4, %ymm6            # ymm6 = ymm4[0,0,2,2]
   3d2d8:      	vshufpd	$0xf, %ymm4, %ymm4, %ymm4 # ymm4 = ymm4[1,1,3,3]
   3d2dd:      	vsubpd	%ymm4, %ymm0, %ymm4
   3d2e1:      	vaddsubpd	%ymm4, %ymm6, %ymm4
   3d2e5:      	vpermpd	$0x44, %ymm4, %ymm6     # ymm6 = ymm4[0,1,0,1]
   3d2eb:      	vsubpd	%ymm4, %ymm0, %ymm8
   3d2ef:      	vperm2f128	$0x31, %ymm8, %ymm4, %ymm4 # ymm4 = ymm4[2,3],ymm8[2,3]
   3d2f5:      	vaddpd	%ymm4, %ymm6, %ymm4
   3d2f9:      	vmovupd	0xa0(%rdi,%rax,8), %ymm6
   3d302:      	vmovddup	%ymm6, %ymm8            # ymm8 = ymm6[0,0,2,2]
   3d306:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm6 # ymm6 = ymm6[1,1,3,3]
   3d30b:      	vsubpd	%ymm6, %ymm0, %ymm6
   3d30f:      	vaddsubpd	%ymm6, %ymm8, %ymm6
   3d313:      	vpermpd	$0x44, %ymm6, %ymm8     # ymm8 = ymm6[0,1,0,1]
   3d319:      	vsubpd	%ymm6, %ymm0, %ymm9
   3d31d:      	vperm2f128	$0x31, %ymm9, %ymm6, %ymm6 # ymm6 = ymm6[2,3],ymm9[2,3]
   3d323:      	vaddpd	%ymm6, %ymm8, %ymm8
   3d327:      	vmovupd	0xc0(%rdi,%rax,8), %ymm6
   3d330:      	vmovddup	%ymm6, %ymm9            # ymm9 = ymm6[0,0,2,2]
   3d334:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm6 # ymm6 = ymm6[1,1,3,3]
   3d339:      	vsubpd	%ymm6, %ymm0, %ymm6
   3d33d:      	vaddsubpd	%ymm6, %ymm9, %ymm6
   3d341:      	vpermpd	$0x44, %ymm6, %ymm9     # ymm9 = ymm6[0,1,0,1]
   3d347:      	vsubpd	%ymm6, %ymm0, %ymm10
   3d34b:      	vperm2f128	$0x31, %ymm10, %ymm6, %ymm6 # ymm6 = ymm6[2,3],ymm10[2,3]
   3d351:      	vaddpd	%ymm6, %ymm9, %ymm6
   3d355:      	vmovupd	0xe0(%rdi,%rax,8), %ymm9
   3d35e:      	vmovddup	%ymm9, %ymm10           # ymm10 = ymm9[0,0,2,2]
   3d363:      	vshufpd	$0xf, %ymm9, %ymm9, %ymm9 # ymm9 = ymm9[1,1,3,3]
   3d369:      	vsubpd	%ymm9, %ymm0, %ymm9
   3d36e:      	vaddsubpd	%ymm9, %ymm10, %ymm9
   3d373:      	vpermpd	$0x44, %ymm9, %ymm10    # ymm10 = ymm9[0,1,0,1]
   3d379:      	vsubpd	%ymm9, %ymm0, %ymm11
   3d37e:      	vperm2f128	$0x31, %ymm11, %ymm9, %ymm9 # ymm9 = ymm9[2,3],ymm11[2,3]
   3d384:      	vaddpd	%ymm9, %ymm10, %ymm9
   3d389:      	vaddpd	%ymm5, %ymm2, %ymm5
   3d38d:      	vsubpd	%ymm7, %ymm3, %ymm7
   3d391:      	vsubpd	%ymm7, %ymm5, %ymm10
   3d395:      	vfmadd213pd	%ymm10, %ymm1, %ymm3 # ymm3 = (ymm1 * ymm3) + ymm10
   3d39a:      	vfmsub213pd	%ymm10, %ymm1, %ymm2 # ymm2 = (ymm1 * ymm2) - ymm10
   3d39f:      	vaddpd	%ymm4, %ymm8, %ymm8
   3d3a3:      	vsubpd	%ymm9, %ymm6, %ymm9
   3d3a8:      	vaddpd	%ymm9, %ymm8, %ymm10
   3d3ad:      	vfnmadd213pd	%ymm10, %ymm1, %ymm6 # ymm6 = -(ymm1 * ymm6) + ymm10
   3d3b2:      	vfmsub213pd	%ymm10, %ymm1, %ymm4 # ymm4 = (ymm1 * ymm4) - ymm10
   3d3b7:      	vaddpd	%ymm6, %ymm3, %ymm10
   3d3bb:      	vfnmadd213pd	%ymm10, %ymm1, %ymm8 # ymm8 = -(ymm1 * ymm8) + ymm10
   3d3c0:      	vfmsub213pd	%ymm10, %ymm1, %ymm5 # ymm5 = (ymm1 * ymm5) - ymm10
   3d3c5:      	vfmsub213pd	%ymm8, %ymm1, %ymm3 # ymm3 = (ymm1 * ymm3) - ymm8
   3d3ca:      	vfmadd213pd	%ymm5, %ymm1, %ymm6 # ymm6 = (ymm1 * ymm6) + ymm5
   3d3cf:      	vaddpd	%ymm4, %ymm2, %ymm10
   3d3d3:      	vfmadd213pd	%ymm10, %ymm1, %ymm9 # ymm9 = (ymm1 * ymm9) + ymm10
   3d3d8:      	vfnmadd213pd	%ymm10, %ymm1, %ymm7 # ymm7 = -(ymm1 * ymm7) + ymm10
   3d3dd:      	vfmsub213pd	%ymm9, %ymm1, %ymm2 # ymm2 = (ymm1 * ymm2) - ymm9
   3d3e2:      	vfnmadd213pd	%ymm7, %ymm1, %ymm4 # ymm4 = -(ymm1 * ymm4) + ymm7
   3d3e7:      	vmovupd	%ymm3, (%rdi,%rax,8)
   3d3ec:      	vmovupd	%ymm9, 0x20(%rdi,%rax,8)
   3d3f2:      	vmovupd	%ymm6, 0x40(%rdi,%rax,8)
   3d3f8:      	vmovupd	%ymm7, 0x60(%rdi,%rax,8)
   3d3fe:      	vmovupd	%ymm8, 0x80(%rdi,%rax,8)
   3d407:      	vmovupd	%ymm2, 0xa0(%rdi,%rax,8)
   3d410:      	vmovupd	%ymm5, 0xc0(%rdi,%rax,8)
   3d419:      	vmovupd	%ymm4, 0xe0(%rdi,%rax,8)
   3d422:      	addq	$0x20, %rax
   3d426:      	cmpq	%rsi, %rax
   3d429:      	jb	0x3d220 <hfirst_g20_nat+0x20>
   3d42f:      	vzeroupper
   3d432:      	retq
   3d433:      	nopw	%cs:(%rax,%rax)

000000000003d440 <hstep_g20_nat>:
   3d440:      	pushq	%r15
   3d442:      	pushq	%r14
   3d444:      	pushq	%r13
   3d446:      	pushq	%r12
   3d448:      	pushq	%rbx
   3d449:      	vmovaps	(%rip), %ymm0           # 0x3d451 <hstep_g20_nat+0x11>
   3d451:      	testq	%rsi, %rsi
   3d454:      	je	0x3d5ae <hstep_g20_nat+0x16e>
   3d45a:      	testq	%rdx, %rdx
   3d45d:      	je	0x3d5ae <hstep_g20_nat+0x16e>
   3d463:      	leaq	(,%rdx,8), %rax
   3d46b:      	movq	%rdx, %rcx
   3d46e:      	shlq	$0x4, %rcx
   3d472:      	leaq	(%rdx,%rdx,2), %r8
   3d476:      	movq	%rdx, %r9
   3d479:      	shlq	$0x5, %r9
   3d47d:      	leaq	(%rdx,%rdx,4), %r14
   3d481:      	leaq	(%rdi,%r8,8), %r10
   3d485:      	shlq	$0x4, %r8
   3d489:      	imulq	$0x38, %rdx, %r11
   3d48d:      	addq	%rdi, %r11
   3d490:      	movq	%rdx, %rbx
   3d493:      	shlq	$0x6, %rbx
   3d497:      	addq	%rdi, %r8
   3d49a:      	leaq	(%rdi,%r14,8), %r14
   3d49e:      	addq	%rdi, %r9
   3d4a1:      	addq	%rdi, %rcx
   3d4a4:      	leaq	(%rdi,%rax), %r15
   3d4a8:      	xorl	%r12d, %r12d
   3d4ab:      	vbroadcastsd	(%rip), %ymm0   # 0x3d4b4 <hstep_g20_nat+0x74>
   3d4b4:      	nopw	%cs:(%rax,%rax)
   3d4c0:      	xorl	%r13d, %r13d
   3d4c3:      	nopw	%cs:(%rax,%rax)
   3d4d0:      	vmovupd	(%rdi,%r13,8), %ymm1
   3d4d6:      	vmovupd	(%rcx,%r13,8), %ymm4
   3d4dc:      	vmovupd	(%r9,%r13,8), %ymm2
   3d4e2:      	vmovupd	(%r8,%r13,8), %ymm5
   3d4e8:      	vaddpd	(%r15,%r13,8), %ymm1, %ymm3
   3d4ee:      	vsubpd	(%r10,%r13,8), %ymm4, %ymm6
   3d4f4:      	vsubpd	%ymm6, %ymm3, %ymm7
   3d4f8:      	vfmadd213pd	%ymm7, %ymm0, %ymm4 # ymm4 = (ymm0 * ymm4) + ymm7
   3d4fd:      	vaddpd	(%r14,%r13,8), %ymm2, %ymm8
   3d503:      	vsubpd	(%r11,%r13,8), %ymm5, %ymm9
   3d509:      	vfmsub213pd	%ymm7, %ymm0, %ymm1 # ymm1 = (ymm0 * ymm1) - ymm7
   3d50e:      	vaddpd	%ymm9, %ymm8, %ymm7
   3d513:      	vfnmadd213pd	%ymm7, %ymm0, %ymm5 # ymm5 = -(ymm0 * ymm5) + ymm7
   3d518:      	vfmsub213pd	%ymm7, %ymm0, %ymm2 # ymm2 = (ymm0 * ymm2) - ymm7
   3d51d:      	vaddpd	%ymm5, %ymm4, %ymm7
   3d521:      	vfnmadd213pd	%ymm7, %ymm0, %ymm8 # ymm8 = -(ymm0 * ymm8) + ymm7
   3d526:      	vfmsub213pd	%ymm7, %ymm0, %ymm3 # ymm3 = (ymm0 * ymm3) - ymm7
   3d52b:      	vfmsub213pd	%ymm8, %ymm0, %ymm4 # ymm4 = (ymm0 * ymm4) - ymm8
   3d530:      	vfmadd213pd	%ymm3, %ymm0, %ymm5 # ymm5 = (ymm0 * ymm5) + ymm3
   3d535:      	vaddpd	%ymm2, %ymm1, %ymm7
   3d539:      	vfmadd213pd	%ymm7, %ymm0, %ymm9 # ymm9 = (ymm0 * ymm9) + ymm7
   3d53e:      	vfnmadd213pd	%ymm7, %ymm0, %ymm6 # ymm6 = -(ymm0 * ymm6) + ymm7
   3d543:      	vfmsub213pd	%ymm9, %ymm0, %ymm1 # ymm1 = (ymm0 * ymm1) - ymm9
   3d548:      	vfnmadd213pd	%ymm6, %ymm0, %ymm2 # ymm2 = -(ymm0 * ymm2) + ymm6
   3d54d:      	vmovupd	%ymm4, (%rdi,%r13,8)
   3d553:      	vmovupd	%ymm9, (%r15,%r13,8)
   3d559:      	vmovupd	%ymm5, (%rcx,%r13,8)
   3d55f:      	vmovupd	%ymm6, (%r10,%r13,8)
   3d565:      	vmovupd	%ymm8, (%r9,%r13,8)
   3d56b:      	vmovupd	%ymm1, (%r14,%r13,8)
   3d571:      	vmovupd	%ymm3, (%r8,%r13,8)
   3d577:      	vmovupd	%ymm2, (%r11,%r13,8)
   3d57d:      	addq	$0x4, %r13
   3d581:      	cmpq	%rdx, %r13
   3d584:      	jb	0x3d4d0 <hstep_g20_nat+0x90>
   3d58a:      	addq	%rax, %r12
   3d58d:      	addq	%rbx, %r11
   3d590:      	addq	%rbx, %r8
   3d593:      	addq	%rbx, %r14
   3d596:      	addq	%rbx, %r9
   3d599:      	addq	%rbx, %r10
   3d59c:      	addq	%rbx, %rcx
   3d59f:      	addq	%rbx, %rdi
   3d5a2:      	addq	%rbx, %r15
   3d5a5:      	cmpq	%rsi, %r12
   3d5a8:      	jb	0x3d4c0 <hstep_g20_nat+0x80>
   3d5ae:      	popq	%rbx
   3d5af:      	popq	%r12
   3d5b1:      	popq	%r13
   3d5b3:      	popq	%r14
   3d5b5:      	popq	%r15
   3d5b7:      	vzeroupper
   3d5ba:      	retq
   3d5bb:      	nopl	(%rax,%rax)

000000000003d5c0 <hfirst_h20_nat>:
   3d5c0:      	vmovaps	(%rip), %ymm0           # 0x3d5c8 <hfirst_h20_nat+0x8>
   3d5c8:      	testq	%rsi, %rsi
   3d5cb:      	je	0x3d7ec <hfirst_h20_nat+0x22c>
   3d5d1:      	xorl	%eax, %eax
   3d5d3:      	vxorpd	%xmm0, %xmm0, %xmm0
   3d5d7:      	vbroadcastsd	(%rip), %ymm1   # 0x3d5e0 <hfirst_h20_nat+0x20>
   3d5e0:      	vmovupd	(%rdi,%rax,8), %ymm2
   3d5e5:      	vmovupd	0x20(%rdi,%rax,8), %ymm4
   3d5eb:      	vmovupd	0x40(%rdi,%rax,8), %ymm5
   3d5f1:      	vmovupd	0x60(%rdi,%rax,8), %ymm6
   3d5f7:      	vmovddup	%ymm2, %ymm3            # ymm3 = ymm2[0,0,2,2]
   3d5fb:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3d600:      	vsubpd	%ymm2, %ymm0, %ymm2
   3d604:      	vaddsubpd	%ymm2, %ymm3, %ymm2
   3d608:      	vpermpd	$0x44, %ymm2, %ymm3     # ymm3 = ymm2[0,1,0,1]
   3d60e:      	vsubpd	%ymm2, %ymm0, %ymm7
   3d612:      	vperm2f128	$0x31, %ymm7, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm7[2,3]
   3d618:      	vaddpd	%ymm2, %ymm3, %ymm3
   3d61c:      	vmovddup	%ymm4, %ymm2            # ymm2 = ymm4[0,0,2,2]
   3d620:      	vshufpd	$0xf, %ymm4, %ymm4, %ymm4 # ymm4 = ymm4[1,1,3,3]
   3d625:      	vsubpd	%ymm4, %ymm0, %ymm4
   3d629:      	vaddsubpd	%ymm4, %ymm2, %ymm2
   3d62d:      	vpermpd	$0x44, %ymm2, %ymm4     # ymm4 = ymm2[0,1,0,1]
   3d633:      	vsubpd	%ymm2, %ymm0, %ymm7
   3d637:      	vperm2f128	$0x31, %ymm7, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm7[2,3]
   3d63d:      	vaddpd	%ymm2, %ymm4, %ymm2
   3d641:      	vmovddup	%ymm5, %ymm4            # ymm4 = ymm5[0,0,2,2]
   3d645:      	vshufpd	$0xf, %ymm5, %ymm5, %ymm5 # ymm5 = ymm5[1,1,3,3]
   3d64a:      	vsubpd	%ymm5, %ymm0, %ymm5
   3d64e:      	vaddsubpd	%ymm5, %ymm4, %ymm4
   3d652:      	vpermpd	$0x44, %ymm4, %ymm5     # ymm5 = ymm4[0,1,0,1]
   3d658:      	vsubpd	%ymm4, %ymm0, %ymm7
   3d65c:      	vperm2f128	$0x31, %ymm7, %ymm4, %ymm4 # ymm4 = ymm4[2,3],ymm7[2,3]
   3d662:      	vaddpd	%ymm4, %ymm5, %ymm5
   3d666:      	vmovddup	%ymm6, %ymm4            # ymm4 = ymm6[0,0,2,2]
   3d66a:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm6 # ymm6 = ymm6[1,1,3,3]
   3d66f:      	vsubpd	%ymm6, %ymm0, %ymm6
   3d673:      	vaddsubpd	%ymm6, %ymm4, %ymm4
   3d677:      	vpermpd	$0x44, %ymm4, %ymm6     # ymm6 = ymm4[0,1,0,1]
   3d67d:      	vsubpd	%ymm4, %ymm0, %ymm7
   3d681:      	vperm2f128	$0x31, %ymm7, %ymm4, %ymm4 # ymm4 = ymm4[2,3],ymm7[2,3]
   3d687:      	vaddpd	%ymm4, %ymm6, %ymm4
   3d68b:      	vmovupd	0x80(%rdi,%rax,8), %ymm6
   3d694:      	vmovddup	%ymm6, %ymm7            # ymm7 = ymm6[0,0,2,2]
   3d698:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm6 # ymm6 = ymm6[1,1,3,3]
   3d69d:      	vsubpd	%ymm6, %ymm0, %ymm6
   3d6a1:      	vaddsubpd	%ymm6, %ymm7, %ymm6
   3d6a5:      	vpermpd	$0x44, %ymm6, %ymm7     # ymm7 = ymm6[0,1,0,1]
   3d6ab:      	vsubpd	%ymm6, %ymm0, %ymm8
   3d6af:      	vperm2f128	$0x31, %ymm8, %ymm6, %ymm6 # ymm6 = ymm6[2,3],ymm8[2,3]
   3d6b5:      	vaddpd	%ymm6, %ymm7, %ymm6
   3d6b9:      	vmovupd	0xa0(%rdi,%rax,8), %ymm7
   3d6c2:      	vmovddup	%ymm7, %ymm8            # ymm8 = ymm7[0,0,2,2]
   3d6c6:      	vshufpd	$0xf, %ymm7, %ymm7, %ymm7 # ymm7 = ymm7[1,1,3,3]
   3d6cb:      	vsubpd	%ymm7, %ymm0, %ymm7
   3d6cf:      	vaddsubpd	%ymm7, %ymm8, %ymm7
   3d6d3:      	vpermpd	$0x44, %ymm7, %ymm8     # ymm8 = ymm7[0,1,0,1]
   3d6d9:      	vsubpd	%ymm7, %ymm0, %ymm9
   3d6dd:      	vperm2f128	$0x31, %ymm9, %ymm7, %ymm7 # ymm7 = ymm7[2,3],ymm9[2,3]
   3d6e3:      	vaddpd	%ymm7, %ymm8, %ymm7
   3d6e7:      	vmovupd	0xc0(%rdi,%rax,8), %ymm8
   3d6f0:      	vmovddup	%ymm8, %ymm9            # ymm9 = ymm8[0,0,2,2]
   3d6f5:      	vshufpd	$0xf, %ymm8, %ymm8, %ymm8 # ymm8 = ymm8[1,1,3,3]
   3d6fb:      	vsubpd	%ymm8, %ymm0, %ymm8
   3d700:      	vaddsubpd	%ymm8, %ymm9, %ymm8
   3d705:      	vpermpd	$0x44, %ymm8, %ymm9     # ymm9 = ymm8[0,1,0,1]
   3d70b:      	vsubpd	%ymm8, %ymm0, %ymm10
   3d710:      	vperm2f128	$0x31, %ymm10, %ymm8, %ymm8 # ymm8 = ymm8[2,3],ymm10[2,3]
   3d716:      	vaddpd	%ymm8, %ymm9, %ymm8
   3d71b:      	vmovupd	0xe0(%rdi,%rax,8), %ymm9
   3d724:      	vmovddup	%ymm9, %ymm10           # ymm10 = ymm9[0,0,2,2]
   3d729:      	vshufpd	$0xf, %ymm9, %ymm9, %ymm9 # ymm9 = ymm9[1,1,3,3]
   3d72f:      	vsubpd	%ymm9, %ymm0, %ymm9
   3d734:      	vaddsubpd	%ymm9, %ymm10, %ymm9
   3d739:      	vpermpd	$0x44, %ymm9, %ymm10    # ymm10 = ymm9[0,1,0,1]
   3d73f:      	vsubpd	%ymm9, %ymm0, %ymm11
   3d744:      	vperm2f128	$0x31, %ymm11, %ymm9, %ymm9 # ymm9 = ymm9[2,3],ymm11[2,3]
   3d74a:      	vaddpd	%ymm9, %ymm10, %ymm9
   3d74f:      	vaddpd	%ymm3, %ymm9, %ymm3
   3d753:      	vaddpd	%ymm2, %ymm8, %ymm10
   3d757:      	vsubpd	%ymm7, %ymm5, %ymm5
   3d75b:      	vsubpd	%ymm6, %ymm4, %ymm11
   3d75f:      	vsubpd	%ymm10, %ymm3, %ymm12
   3d764:      	vaddpd	%ymm5, %ymm11, %ymm13
   3d768:      	vsubpd	%ymm13, %ymm12, %ymm14
   3d76d:      	vmulpd	%ymm1, %ymm14, %ymm14
   3d771:      	vsubpd	%ymm9, %ymm14, %ymm9
   3d776:      	vsubpd	%ymm7, %ymm14, %ymm7
   3d77a:      	vaddpd	%ymm9, %ymm8, %ymm8
   3d77f:      	vsubpd	%ymm6, %ymm7, %ymm6
   3d783:      	vaddpd	%ymm8, %ymm11, %ymm11
   3d788:      	vaddpd	%ymm7, %ymm4, %ymm4
   3d78c:      	vsubpd	%ymm4, %ymm12, %ymm7
   3d790:      	vaddpd	%ymm5, %ymm8, %ymm5
   3d794:      	vaddpd	%ymm6, %ymm10, %ymm8
   3d798:      	vaddpd	%ymm2, %ymm9, %ymm2
   3d79c:      	vaddpd	%ymm2, %ymm13, %ymm9
   3d7a0:      	vsubpd	%ymm6, %ymm3, %ymm3
   3d7a4:      	vmovupd	%ymm3, (%rdi,%rax,8)
   3d7a9:      	vmovupd	%ymm5, 0x20(%rdi,%rax,8)
   3d7af:      	vmovupd	%ymm2, 0x40(%rdi,%rax,8)
   3d7b5:      	vmovupd	%ymm4, 0x60(%rdi,%rax,8)
   3d7bb:      	vmovupd	%ymm9, 0x80(%rdi,%rax,8)
   3d7c4:      	vmovupd	%ymm7, 0xa0(%rdi,%rax,8)
   3d7cd:      	vmovupd	%ymm8, 0xc0(%rdi,%rax,8)
   3d7d6:      	vmovupd	%ymm11, 0xe0(%rdi,%rax,8)
   3d7df:      	addq	$0x20, %rax
   3d7e3:      	cmpq	%rsi, %rax
   3d7e6:      	jb	0x3d5e0 <hfirst_h20_nat+0x20>
   3d7ec:      	vzeroupper
   3d7ef:      	retq

000000000003d7f0 <hstep_h20_nat>:
   3d7f0:      	pushq	%r15
   3d7f2:      	pushq	%r14
   3d7f4:      	pushq	%r13
   3d7f6:      	pushq	%r12
   3d7f8:      	pushq	%rbx
   3d7f9:      	vmovaps	(%rip), %ymm0           # 0x3d801 <hstep_h20_nat+0x11>
   3d801:      	testq	%rsi, %rsi
   3d804:      	je	0x3d95f <hstep_h20_nat+0x16f>
   3d80a:      	testq	%rdx, %rdx
   3d80d:      	je	0x3d95f <hstep_h20_nat+0x16f>
   3d813:      	leaq	(,%rdx,8), %rax
   3d81b:      	movq	%rdx, %rcx
   3d81e:      	shlq	$0x4, %rcx
   3d822:      	leaq	(%rdx,%rdx,2), %r8
   3d826:      	movq	%rdx, %r9
   3d829:      	shlq	$0x5, %r9
   3d82d:      	leaq	(%rdx,%rdx,4), %r14
   3d831:      	leaq	(%rdi,%r8,8), %r10
   3d835:      	shlq	$0x4, %r8
   3d839:      	imulq	$0x38, %rdx, %r11
   3d83d:      	addq	%rdi, %r11
   3d840:      	movq	%rdx, %rbx
   3d843:      	shlq	$0x6, %rbx
   3d847:      	addq	%rdi, %r8
   3d84a:      	leaq	(%rdi,%r14,8), %r14
   3d84e:      	addq	%rdi, %r9
   3d851:      	addq	%rdi, %rcx
   3d854:      	leaq	(%rdi,%rax), %r15
   3d858:      	xorl	%r12d, %r12d
   3d85b:      	vbroadcastsd	(%rip), %ymm0   # 0x3d864 <hstep_h20_nat+0x74>
   3d864:      	nopw	%cs:(%rax,%rax)
   3d870:      	xorl	%r13d, %r13d
   3d873:      	nopw	%cs:(%rax,%rax)
   3d880:      	vmovupd	(%r15,%r13,8), %ymm1
   3d886:      	vmovupd	(%rcx,%r13,8), %ymm2
   3d88c:      	vmovupd	(%r10,%r13,8), %ymm3
   3d892:      	vmovupd	(%r9,%r13,8), %ymm4
   3d898:      	vmovupd	(%r14,%r13,8), %ymm5
   3d89e:      	vmovupd	(%r8,%r13,8), %ymm6
   3d8a4:      	vmovupd	(%r11,%r13,8), %ymm7
   3d8aa:      	vaddpd	(%rdi,%r13,8), %ymm7, %ymm8
   3d8b0:      	vaddpd	%ymm6, %ymm1, %ymm9
   3d8b4:      	vsubpd	%ymm5, %ymm2, %ymm2
   3d8b8:      	vsubpd	%ymm4, %ymm3, %ymm10
   3d8bc:      	vsubpd	%ymm9, %ymm8, %ymm11
   3d8c1:      	vaddpd	%ymm2, %ymm10, %ymm12
   3d8c5:      	vsubpd	%ymm12, %ymm11, %ymm13
   3d8ca:      	vmulpd	%ymm0, %ymm13, %ymm13
   3d8ce:      	vsubpd	%ymm7, %ymm13, %ymm7
   3d8d2:      	vsubpd	%ymm5, %ymm13, %ymm5
   3d8d6:      	vaddpd	%ymm7, %ymm6, %ymm6
   3d8da:      	vsubpd	%ymm4, %ymm5, %ymm4
   3d8de:      	vaddpd	%ymm6, %ymm10, %ymm10
   3d8e2:      	vaddpd	%ymm5, %ymm3, %ymm3
   3d8e6:      	vsubpd	%ymm3, %ymm11, %ymm5
   3d8ea:      	vaddpd	%ymm6, %ymm2, %ymm2
   3d8ee:      	vaddpd	%ymm4, %ymm9, %ymm6
   3d8f2:      	vaddpd	%ymm7, %ymm1, %ymm1
   3d8f6:      	vaddpd	%ymm1, %ymm12, %ymm7
   3d8fa:      	vsubpd	%ymm4, %ymm8, %ymm4
   3d8fe:      	vmovupd	%ymm4, (%rdi,%r13,8)
   3d904:      	vmovupd	%ymm2, (%r15,%r13,8)
   3d90a:      	vmovupd	%ymm1, (%rcx,%r13,8)
   3d910:      	vmovupd	%ymm3, (%r10,%r13,8)
   3d916:      	vmovupd	%ymm7, (%r9,%r13,8)
   3d91c:      	vmovupd	%ymm5, (%r14,%r13,8)
   3d922:      	vmovupd	%ymm6, (%r8,%r13,8)
   3d928:      	vmovupd	%ymm10, (%r11,%r13,8)
   3d92e:      	addq	$0x4, %r13
   3d932:      	cmpq	%rdx, %r13
   3d935:      	jb	0x3d880 <hstep_h20_nat+0x90>
   3d93b:      	addq	%rax, %r12
   3d93e:      	addq	%rbx, %r11
   3d941:      	addq	%rbx, %r8
   3d944:      	addq	%rbx, %r14
   3d947:      	addq	%rbx, %r9
   3d94a:      	addq	%rbx, %r10
   3d94d:      	addq	%rbx, %rcx
   3d950:      	addq	%rbx, %rdi
   3d953:      	addq	%rbx, %r15
   3d956:      	cmpq	%rsi, %r12
   3d959:      	jb	0x3d870 <hstep_h20_nat+0x80>
   3d95f:      	popq	%rbx
   3d960:      	popq	%r12
   3d962:      	popq	%r13
   3d964:      	popq	%r14
   3d966:      	popq	%r15
   3d968:      	vzeroupper
   3d96b:      	retq
   3d96c:      	nopl	(%rax)

000000000003d970 <hfirst_g52_nat>:
   3d970:      	subq	$0x48, %rsp
   3d974:      	vmovaps	(%rip), %ymm0           # 0x3d97c <hfirst_g52_nat+0xc>
   3d97c:      	testq	%rsi, %rsi
   3d97f:      	je	0x3de82 <hfirst_g52_nat+0x512>
   3d985:      	xorl	%eax, %eax
   3d987:      	nopw	(%rax,%rax)
   3d990:      	vmovupd	(%rdi,%rax,8), %ymm0
   3d995:      	vmovupd	0x20(%rdi,%rax,8), %ymm2
   3d99b:      	vmovupd	0x40(%rdi,%rax,8), %ymm4
   3d9a1:      	vmovupd	0x60(%rdi,%rax,8), %ymm5
   3d9a7:      	vmovddup	%ymm0, %ymm6            # ymm6 = ymm0[0,0,2,2]
   3d9ab:      	vshufpd	$0xf, %ymm0, %ymm0, %ymm0 # ymm0 = ymm0[1,1,3,3]
   3d9b0:      	vxorpd	%xmm3, %xmm3, %xmm3
   3d9b4:      	vsubpd	%ymm0, %ymm3, %ymm0
   3d9b8:      	vaddsubpd	%ymm0, %ymm6, %ymm0
   3d9bc:      	vpermpd	$0x44, %ymm0, %ymm6     # ymm6 = ymm0[0,1,0,1]
   3d9c2:      	vsubpd	%ymm0, %ymm3, %ymm7
   3d9c6:      	vperm2f128	$0x31, %ymm7, %ymm0, %ymm0 # ymm0 = ymm0[2,3],ymm7[2,3]
   3d9cc:      	vaddpd	%ymm0, %ymm6, %ymm1
   3d9d0:      	vmovddup	%ymm2, %ymm0            # ymm0 = ymm2[0,0,2,2]
   3d9d4:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3d9d9:      	vsubpd	%ymm2, %ymm3, %ymm2
   3d9dd:      	vaddsubpd	%ymm2, %ymm0, %ymm0
   3d9e1:      	vpermpd	$0x44, %ymm0, %ymm2     # ymm2 = ymm0[0,1,0,1]
   3d9e7:      	vsubpd	%ymm0, %ymm3, %ymm6
   3d9eb:      	vperm2f128	$0x31, %ymm6, %ymm0, %ymm0 # ymm0 = ymm0[2,3],ymm6[2,3]
   3d9f1:      	vaddpd	%ymm0, %ymm2, %ymm8
   3d9f5:      	vmovddup	%ymm4, %ymm0            # ymm0 = ymm4[0,0,2,2]
   3d9f9:      	vshufpd	$0xf, %ymm4, %ymm4, %ymm2 # ymm2 = ymm4[1,1,3,3]
   3d9fe:      	vsubpd	%ymm2, %ymm3, %ymm2
   3da02:      	vaddsubpd	%ymm2, %ymm0, %ymm0
   3da06:      	vpermpd	$0x44, %ymm0, %ymm2     # ymm2 = ymm0[0,1,0,1]
   3da0c:      	vsubpd	%ymm0, %ymm3, %ymm4
   3da10:      	vperm2f128	$0x31, %ymm4, %ymm0, %ymm0 # ymm0 = ymm0[2,3],ymm4[2,3]
   3da16:      	vaddpd	%ymm0, %ymm2, %ymm0
   3da1a:      	vmovupd	%ymm0, -0x80(%rsp)
   3da20:      	vmovddup	%ymm5, %ymm0            # ymm0 = ymm5[0,0,2,2]
   3da24:      	vshufpd	$0xf, %ymm5, %ymm5, %ymm2 # ymm2 = ymm5[1,1,3,3]
   3da29:      	vsubpd	%ymm2, %ymm3, %ymm2
   3da2d:      	vaddsubpd	%ymm2, %ymm0, %ymm0
   3da31:      	vpermpd	$0x44, %ymm0, %ymm2     # ymm2 = ymm0[0,1,0,1]
   3da37:      	vsubpd	%ymm0, %ymm3, %ymm4
   3da3b:      	vperm2f128	$0x31, %ymm4, %ymm0, %ymm0 # ymm0 = ymm0[2,3],ymm4[2,3]
   3da41:      	vaddpd	%ymm0, %ymm2, %ymm10
   3da45:      	vmovupd	0x80(%rdi,%rax,8), %ymm0
   3da4e:      	vmovddup	%ymm0, %ymm2            # ymm2 = ymm0[0,0,2,2]
   3da52:      	vshufpd	$0xf, %ymm0, %ymm0, %ymm0 # ymm0 = ymm0[1,1,3,3]
   3da57:      	vsubpd	%ymm0, %ymm3, %ymm0
   3da5b:      	vaddsubpd	%ymm0, %ymm2, %ymm0
   3da5f:      	vpermpd	$0x44, %ymm0, %ymm2     # ymm2 = ymm0[0,1,0,1]
   3da65:      	vsubpd	%ymm0, %ymm3, %ymm4
   3da69:      	vperm2f128	$0x31, %ymm4, %ymm0, %ymm0 # ymm0 = ymm0[2,3],ymm4[2,3]
   3da6f:      	vaddpd	%ymm0, %ymm2, %ymm0
   3da73:      	vmovupd	%ymm0, -0x20(%rsp)
   3da79:      	vmovupd	0xa0(%rdi,%rax,8), %ymm0
   3da82:      	vmovddup	%ymm0, %ymm2            # ymm2 = ymm0[0,0,2,2]
   3da86:      	vshufpd	$0xf, %ymm0, %ymm0, %ymm0 # ymm0 = ymm0[1,1,3,3]
   3da8b:      	vsubpd	%ymm0, %ymm3, %ymm0
   3da8f:      	vaddsubpd	%ymm0, %ymm2, %ymm0
   3da93:      	vpermpd	$0x44, %ymm0, %ymm2     # ymm2 = ymm0[0,1,0,1]
   3da99:      	vsubpd	%ymm0, %ymm3, %ymm5
   3da9d:      	vperm2f128	$0x31, %ymm5, %ymm0, %ymm0 # ymm0 = ymm0[2,3],ymm5[2,3]
   3daa3:      	vaddpd	%ymm0, %ymm2, %ymm0
   3daa7:      	vmovupd	%ymm0, -0x60(%rsp)
   3daad:      	vmovupd	0xc0(%rdi,%rax,8), %ymm2
   3dab6:      	vmovddup	%ymm2, %ymm5            # ymm5 = ymm2[0,0,2,2]
   3daba:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3dabf:      	vsubpd	%ymm2, %ymm3, %ymm2
   3dac3:      	vaddsubpd	%ymm2, %ymm5, %ymm2
   3dac7:      	vpermpd	$0x44, %ymm2, %ymm5     # ymm5 = ymm2[0,1,0,1]
   3dacd:      	vsubpd	%ymm2, %ymm3, %ymm6
   3dad1:      	vperm2f128	$0x31, %ymm6, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm6[2,3]
   3dad7:      	vaddpd	%ymm2, %ymm5, %ymm0
   3dadb:      	vmovupd	%ymm0, -0x40(%rsp)
   3dae1:      	vmovupd	0xe0(%rdi,%rax,8), %ymm2
   3daea:      	vmovddup	%ymm2, %ymm6            # ymm6 = ymm2[0,0,2,2]
   3daee:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3daf3:      	vsubpd	%ymm2, %ymm3, %ymm2
   3daf7:      	vaddsubpd	%ymm2, %ymm6, %ymm2
   3dafb:      	vpermpd	$0x44, %ymm2, %ymm6     # ymm6 = ymm2[0,1,0,1]
   3db01:      	vsubpd	%ymm2, %ymm3, %ymm7
   3db05:      	vperm2f128	$0x31, %ymm7, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm7[2,3]
   3db0b:      	vaddpd	%ymm2, %ymm6, %ymm15
   3db0f:      	vmovupd	0x100(%rdi,%rax,8), %ymm2
   3db18:      	vmovddup	%ymm2, %ymm6            # ymm6 = ymm2[0,0,2,2]
   3db1c:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3db21:      	vsubpd	%ymm2, %ymm3, %ymm2
   3db25:      	vaddsubpd	%ymm2, %ymm6, %ymm2
   3db29:      	vpermpd	$0x44, %ymm2, %ymm6     # ymm6 = ymm2[0,1,0,1]
   3db2f:      	vsubpd	%ymm2, %ymm3, %ymm7
   3db33:      	vperm2f128	$0x31, %ymm7, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm7[2,3]
   3db39:      	vaddpd	%ymm2, %ymm6, %ymm0
   3db3d:      	vmovupd	%ymm0, 0x20(%rsp)
   3db43:      	vmovupd	0x120(%rdi,%rax,8), %ymm2
   3db4c:      	vmovddup	%ymm2, %ymm7            # ymm7 = ymm2[0,0,2,2]
   3db50:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3db55:      	vsubpd	%ymm2, %ymm3, %ymm2
   3db59:      	vaddsubpd	%ymm2, %ymm7, %ymm2
   3db5d:      	vpermpd	$0x44, %ymm2, %ymm7     # ymm7 = ymm2[0,1,0,1]
   3db63:      	vsubpd	%ymm2, %ymm3, %ymm9
   3db67:      	vperm2f128	$0x31, %ymm9, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm9[2,3]
   3db6d:      	vaddpd	%ymm2, %ymm7, %ymm11
   3db71:      	vmovupd	0x140(%rdi,%rax,8), %ymm2
   3db7a:      	vmovddup	%ymm2, %ymm7            # ymm7 = ymm2[0,0,2,2]
   3db7e:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3db83:      	vsubpd	%ymm2, %ymm3, %ymm2
   3db87:      	vaddsubpd	%ymm2, %ymm7, %ymm2
   3db8b:      	vpermpd	$0x44, %ymm2, %ymm7     # ymm7 = ymm2[0,1,0,1]
   3db91:      	vsubpd	%ymm2, %ymm3, %ymm9
   3db95:      	vperm2f128	$0x31, %ymm9, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm9[2,3]
   3db9b:      	vaddpd	%ymm2, %ymm7, %ymm7
   3db9f:      	vmovupd	0x160(%rdi,%rax,8), %ymm2
   3dba8:      	vmovddup	%ymm2, %ymm9            # ymm9 = ymm2[0,0,2,2]
   3dbac:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3dbb1:      	vsubpd	%ymm2, %ymm3, %ymm2
   3dbb5:      	vaddsubpd	%ymm2, %ymm9, %ymm2
   3dbb9:      	vpermpd	$0x44, %ymm2, %ymm9     # ymm9 = ymm2[0,1,0,1]
   3dbbf:      	vsubpd	%ymm2, %ymm3, %ymm12
   3dbc3:      	vperm2f128	$0x31, %ymm12, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm12[2,3]
   3dbc9:      	vaddpd	%ymm2, %ymm9, %ymm13
   3dbcd:      	vmovupd	0x180(%rdi,%rax,8), %ymm2
   3dbd6:      	vmovddup	%ymm2, %ymm9            # ymm9 = ymm2[0,0,2,2]
   3dbda:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3dbdf:      	vsubpd	%ymm2, %ymm3, %ymm2
   3dbe3:      	vaddsubpd	%ymm2, %ymm9, %ymm2
   3dbe7:      	vpermpd	$0x44, %ymm2, %ymm9     # ymm9 = ymm2[0,1,0,1]
   3dbed:      	vsubpd	%ymm2, %ymm3, %ymm12
   3dbf1:      	vperm2f128	$0x31, %ymm12, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm12[2,3]
   3dbf7:      	vaddpd	%ymm2, %ymm9, %ymm9
   3dbfb:      	vmovupd	0x1a0(%rdi,%rax,8), %ymm2
   3dc04:      	vmovddup	%ymm2, %ymm12           # ymm12 = ymm2[0,0,2,2]
   3dc08:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3dc0d:      	vsubpd	%ymm2, %ymm3, %ymm2
   3dc11:      	vaddsubpd	%ymm2, %ymm12, %ymm2
   3dc15:      	vpermpd	$0x44, %ymm2, %ymm12    # ymm12 = ymm2[0,1,0,1]
   3dc1b:      	vsubpd	%ymm2, %ymm3, %ymm14
   3dc1f:      	vperm2f128	$0x31, %ymm14, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm14[2,3]
   3dc25:      	vaddpd	%ymm2, %ymm12, %ymm0
   3dc29:      	vmovupd	%ymm0, (%rsp)
   3dc2e:      	vmovupd	0x1c0(%rdi,%rax,8), %ymm12
   3dc37:      	vmovddup	%ymm12, %ymm14          # ymm14 = ymm12[0,0,2,2]
   3dc3c:      	vshufpd	$0xf, %ymm12, %ymm12, %ymm12 # ymm12 = ymm12[1,1,3,3]
   3dc42:      	vsubpd	%ymm12, %ymm3, %ymm12
   3dc47:      	vaddsubpd	%ymm12, %ymm14, %ymm12
   3dc4c:      	vsubpd	%ymm12, %ymm3, %ymm14
   3dc51:      	vperm2f128	$0x31, %ymm14, %ymm12, %ymm14 # ymm14 = ymm12[2,3],ymm14[2,3]
   3dc57:      	vpermpd	$0x44, %ymm12, %ymm12   # ymm12 = ymm12[0,1,0,1]
   3dc5d:      	vaddpd	%ymm14, %ymm12, %ymm12
   3dc62:      	vmovupd	0x1e0(%rdi,%rax,8), %ymm14
   3dc6b:      	vmovddup	%ymm14, %ymm0           # ymm0 = ymm14[0,0,2,2]
   3dc70:      	vshufpd	$0xf, %ymm14, %ymm14, %ymm14 # ymm14 = ymm14[1,1,3,3]
   3dc76:      	vsubpd	%ymm14, %ymm3, %ymm14
   3dc7b:      	vaddsubpd	%ymm14, %ymm0, %ymm0
   3dc80:      	vsubpd	%ymm0, %ymm3, %ymm14
   3dc84:      	vperm2f128	$0x31, %ymm14, %ymm0, %ymm14 # ymm14 = ymm0[2,3],ymm14[2,3]
   3dc8a:      	vpermpd	$0x44, %ymm0, %ymm0     # ymm0 = ymm0[0,1,0,1]
   3dc90:      	vaddpd	%ymm0, %ymm14, %ymm14
   3dc94:      	vmovapd	%ymm1, %ymm4
   3dc98:      	vaddpd	%ymm1, %ymm8, %ymm8
   3dc9c:      	vmovupd	-0x80(%rsp), %ymm5
   3dca2:      	vsubpd	%ymm10, %ymm5, %ymm10
   3dca7:      	vsubpd	%ymm10, %ymm8, %ymm1
   3dcac:      	vbroadcastsd	(%rip), %ymm2   # 0x3dcb5 <hfirst_g52_nat+0x345>
   3dcb5:      	vfmadd213pd	%ymm1, %ymm2, %ymm5 # ymm5 = (ymm2 * ymm5) + ymm1
   3dcba:      	vmovupd	%ymm5, -0x80(%rsp)
   3dcc0:      	vfmsub213pd	%ymm1, %ymm2, %ymm4 # ymm4 = (ymm2 * ymm4) - ymm1
   3dcc5:      	vmovupd	-0x20(%rsp), %ymm1
   3dccb:      	vaddpd	-0x60(%rsp), %ymm1, %ymm6
   3dcd1:      	vmovupd	-0x40(%rsp), %ymm0
   3dcd7:      	vsubpd	%ymm15, %ymm0, %ymm15
   3dcdc:      	vaddpd	%ymm6, %ymm15, %ymm3
   3dce0:      	vfnmadd213pd	%ymm3, %ymm2, %ymm0 # ymm0 = -(ymm2 * ymm0) + ymm3
   3dce5:      	vmovupd	%ymm0, -0x40(%rsp)
   3dceb:      	vfmsub213pd	%ymm3, %ymm2, %ymm1 # ymm1 = (ymm2 * ymm1) - ymm3
   3dcf0:      	vmovupd	%ymm1, -0x20(%rsp)
   3dcf6:      	vsubpd	%ymm0, %ymm5, %ymm3
   3dcfa:      	vfmadd213pd	%ymm3, %ymm2, %ymm6 # ymm6 = (ymm2 * ymm6) + ymm3
   3dcff:      	vfmsub213pd	%ymm3, %ymm2, %ymm8 # ymm8 = (ymm2 * ymm8) - ymm3
   3dd04:      	vaddpd	%ymm1, %ymm4, %ymm3
   3dd08:      	vfmadd213pd	%ymm3, %ymm2, %ymm15 # ymm15 = (ymm2 * ymm15) + ymm3
   3dd0d:      	vfnmadd213pd	%ymm3, %ymm2, %ymm10 # ymm10 = -(ymm2 * ymm10) + ymm3
   3dd12:      	vmovupd	0x20(%rsp), %ymm5
   3dd18:      	vaddpd	%ymm5, %ymm11, %ymm11
   3dd1c:      	vsubpd	%ymm13, %ymm7, %ymm13
   3dd21:      	vsubpd	%ymm13, %ymm11, %ymm3
   3dd26:      	vfmadd213pd	%ymm3, %ymm2, %ymm7 # ymm7 = (ymm2 * ymm7) + ymm3
   3dd2b:      	vfmsub213pd	%ymm3, %ymm2, %ymm5 # ymm5 = (ymm2 * ymm5) - ymm3
   3dd30:      	vaddpd	(%rsp), %ymm9, %ymm0
   3dd35:      	vsubpd	%ymm14, %ymm12, %ymm14
   3dd3a:      	vaddpd	%ymm0, %ymm14, %ymm3
   3dd3e:      	vfnmadd213pd	%ymm3, %ymm2, %ymm12 # ymm12 = -(ymm2 * ymm12) + ymm3
   3dd43:      	vfmsub213pd	%ymm3, %ymm2, %ymm9 # ymm9 = (ymm2 * ymm9) - ymm3
   3dd48:      	vaddpd	%ymm7, %ymm12, %ymm3
   3dd4c:      	vfnmadd213pd	%ymm3, %ymm2, %ymm0 # ymm0 = -(ymm2 * ymm0) + ymm3
   3dd51:      	vfmsub213pd	%ymm3, %ymm2, %ymm11 # ymm11 = (ymm2 * ymm11) - ymm3
   3dd56:      	vsubpd	%ymm9, %ymm5, %ymm3
   3dd5b:      	vfnmadd213pd	%ymm3, %ymm2, %ymm14 # ymm14 = -(ymm2 * ymm14) + ymm3
   3dd60:      	vfnmadd213pd	%ymm3, %ymm2, %ymm13 # ymm13 = -(ymm2 * ymm13) + ymm3
   3dd65:      	vaddpd	%ymm0, %ymm6, %ymm3
   3dd69:      	vfnmadd213pd	%ymm3, %ymm2, %ymm7 # ymm7 = -(ymm2 * ymm7) + ymm3
   3dd6e:      	vmovupd	-0x80(%rsp), %ymm1
   3dd74:      	vfmsub213pd	%ymm3, %ymm2, %ymm1 # ymm1 = (ymm2 * ymm1) - ymm3
   3dd79:      	vmovupd	%ymm1, -0x80(%rsp)
   3dd7f:      	vaddpd	%ymm14, %ymm15, %ymm3
   3dd84:      	vfnmadd213pd	%ymm3, %ymm2, %ymm5 # ymm5 = -(ymm2 * ymm5) + ymm3
   3dd89:      	vfmsub213pd	%ymm3, %ymm2, %ymm4 # ymm4 = (ymm2 * ymm4) - ymm3
   3dd8e:      	vmovupd	%ymm4, -0x60(%rsp)
   3dd94:      	vaddpd	%ymm11, %ymm8, %ymm3
   3dd99:      	vfmadd213pd	%ymm3, %ymm2, %ymm12 # ymm12 = (ymm2 * ymm12) + ymm3
   3dd9e:      	vmovupd	-0x40(%rsp), %ymm4
   3dda4:      	vfnmadd213pd	%ymm3, %ymm2, %ymm4 # ymm4 = -(ymm2 * ymm4) + ymm3
   3dda9:      	vaddpd	%ymm13, %ymm10, %ymm3
   3ddae:      	vfmadd213pd	%ymm3, %ymm2, %ymm9 # ymm9 = (ymm2 * ymm9) + ymm3
   3ddb3:      	vmovupd	-0x20(%rsp), %ymm1
   3ddb9:      	vfnmadd213pd	%ymm3, %ymm2, %ymm1 # ymm1 = -(ymm2 * ymm1) + ymm3
   3ddbe:      	vfmsub213pd	%ymm7, %ymm2, %ymm6 # ymm6 = (ymm2 * ymm6) - ymm7
   3ddc3:      	vmovupd	%ymm6, (%rdi,%rax,8)
   3ddc8:      	vfmsub213pd	%ymm5, %ymm2, %ymm15 # ymm15 = (ymm2 * ymm15) - ymm5
   3ddcd:      	vmovupd	%ymm15, 0x20(%rdi,%rax,8)
   3ddd3:      	vfmsub213pd	%ymm12, %ymm2, %ymm8 # ymm8 = (ymm2 * ymm8) - ymm12
   3ddd8:      	vmovupd	%ymm12, 0x40(%rdi,%rax,8)
   3ddde:      	vfmsub213pd	%ymm9, %ymm2, %ymm10 # ymm10 = (ymm2 * ymm10) - ymm9
   3dde3:      	vmovupd	%ymm9, 0x60(%rdi,%rax,8)
   3dde9:      	vmovupd	-0x80(%rsp), %ymm3
   3ddef:      	vfmadd213pd	%ymm3, %ymm2, %ymm0 # ymm0 = (ymm2 * ymm0) + ymm3
   3ddf4:      	vmovupd	%ymm0, 0x80(%rdi,%rax,8)
   3ddfd:      	vmovupd	-0x60(%rsp), %ymm6
   3de03:      	vfmadd213pd	%ymm6, %ymm2, %ymm14 # ymm14 = (ymm2 * ymm14) + ymm6
   3de08:      	vmovupd	%ymm14, 0xa0(%rdi,%rax,8)
   3de11:      	vfnmadd213pd	%ymm4, %ymm2, %ymm11 # ymm11 = -(ymm2 * ymm11) + ymm4
   3de16:      	vmovupd	%ymm4, 0xc0(%rdi,%rax,8)
   3de1f:      	vfnmadd213pd	%ymm1, %ymm2, %ymm13 # ymm13 = -(ymm2 * ymm13) + ymm1
   3de24:      	vmovupd	%ymm1, 0xe0(%rdi,%rax,8)
   3de2d:      	vmovupd	%ymm7, 0x100(%rdi,%rax,8)
   3de36:      	vmovupd	%ymm5, 0x120(%rdi,%rax,8)
   3de3f:      	vmovupd	%ymm8, 0x140(%rdi,%rax,8)
   3de48:      	vmovupd	%ymm10, 0x160(%rdi,%rax,8)
   3de51:      	vmovupd	%ymm3, 0x180(%rdi,%rax,8)
   3de5a:      	vmovupd	%ymm6, 0x1a0(%rdi,%rax,8)
   3de63:      	vmovupd	%ymm11, 0x1c0(%rdi,%rax,8)
   3de6c:      	vmovupd	%ymm13, 0x1e0(%rdi,%rax,8)
   3de75:      	addq	$0x40, %rax
   3de79:      	cmpq	%rsi, %rax
   3de7c:      	jb	0x3d990 <hfirst_g52_nat+0x20>
   3de82:      	addq	$0x48, %rsp
   3de86:      	vzeroupper
   3de89:      	retq
   3de8a:      	nopw	(%rax,%rax)

000000000003de90 <hstep_g52_nat>:
   3de90:      	pushq	%rbp
   3de91:      	pushq	%r15
   3de93:      	pushq	%r14
   3de95:      	pushq	%r13
   3de97:      	pushq	%r12
   3de99:      	pushq	%rbx
   3de9a:      	subq	$0x98, %rsp
   3dea1:      	movq	%rdx, -0x70(%rsp)
   3dea6:      	vmovaps	(%rip), %ymm0           # 0x3deae <hstep_g52_nat+0x1e>
   3deae:      	movq	%rsi, 0x28(%rsp)
   3deb3:      	testq	%rsi, %rsi
   3deb6:      	je	0x3e2ac <hstep_g52_nat+0x41c>
   3debc:      	cmpq	$0x0, -0x70(%rsp)
   3dec2:      	je	0x3e2ac <hstep_g52_nat+0x41c>
   3dec8:      	movq	%rdi, %r14
   3decb:      	movq	-0x70(%rsp), %rax
   3ded0:      	movq	%rax, %rcx
   3ded3:      	shlq	$0x4, %rcx
   3ded7:      	movq	%rcx, -0x58(%rsp)
   3dedc:      	leaq	(%rax,%rax,2), %r9
   3dee0:      	movq	%rax, %rcx
   3dee3:      	shlq	$0x5, %rcx
   3dee7:      	movq	%rcx, -0x78(%rsp)
   3deec:      	leaq	(%rax,%rax,4), %r12
   3def0:      	movq	%r9, %rsi
   3def3:      	leaq	(%rdi,%r9,8), %rcx
   3def7:      	shlq	$0x4, %r9
   3defb:      	movq	%rax, %r8
   3defe:      	imulq	$0x38, %rax, %rbx
   3df02:      	movq	%rax, %r10
   3df05:      	shlq	$0x6, %r10
   3df09:      	leaq	(%rax,%rax,8), %rax
   3df0d:      	movq	%rax, 0x30(%rsp)
   3df12:      	leaq	(%rdi,%r12,8), %r13
   3df16:      	shlq	$0x4, %r12
   3df1a:      	imulq	$0x58, %r8, %rbp
   3df1e:      	shlq	$0x5, %rsi
   3df22:      	imulq	$0x68, %r8, %rax
   3df26:      	imulq	$0x70, %r8, %rdx
   3df2a:      	imulq	$0x78, %r8, %rdi
   3df2e:      	addq	%r14, %rdi
   3df31:      	movq	%rdi, -0x48(%rsp)
   3df36:      	movq	%r8, %r11
   3df39:      	movq	%r8, %rdi
   3df3c:      	shlq	$0x7, %r11
   3df40:      	movq	%r11, 0x20(%rsp)
   3df45:      	addq	%r14, %rdx
   3df48:      	movq	%rdx, -0x68(%rsp)
   3df4d:      	addq	%r14, %rax
   3df50:      	addq	%r14, %rsi
   3df53:      	movq	%rsi, %r11
   3df56:      	addq	%r14, %rbp
   3df59:      	addq	%r14, %r12
   3df5c:      	movq	%r12, %r15
   3df5f:      	movq	0x30(%rsp), %rdx
   3df64:      	leaq	(%r14,%rdx,8), %r8
   3df68:      	addq	%r14, %r10
   3df6b:      	movq	%r10, %r12
   3df6e:      	addq	%r14, %rbx
   3df71:      	addq	%r14, %r9
   3df74:      	movq	%r9, %r10
   3df77:      	vbroadcastsd	(%rip), %ymm8   # 0x3df80 <hstep_g52_nat+0xf0>
   3df80:      	movq	-0x78(%rsp), %r9
   3df85:      	addq	%r14, %r9
   3df88:      	movq	-0x58(%rsp), %rsi
   3df8d:      	addq	%r14, %rsi
   3df90:      	leaq	(%r14,%rdi,8), %rdi
   3df94:      	movq	%rdi, -0x40(%rsp)
   3df99:      	movq	$0x0, -0x50(%rsp)
   3dfa2:      	nopw	%cs:(%rax,%rax)
   3dfb0:      	movq	%rax, -0x38(%rsp)
   3dfb5:      	movq	%rbp, -0x30(%rsp)
   3dfba:      	movq	%r11, -0x60(%rsp)
   3dfbf:      	movq	%r15, -0x28(%rsp)
   3dfc4:      	movq	%r8, -0x20(%rsp)
   3dfc9:      	movq	%r12, -0x18(%rsp)
   3dfce:      	movq	%rbx, -0x10(%rsp)
   3dfd3:      	movq	%r10, -0x8(%rsp)
   3dfd8:      	movq	%r13, (%rsp)
   3dfdc:      	movq	%rsi, 0x8(%rsp)
   3dfe1:      	movq	%r9, -0x78(%rsp)
   3dfe6:      	movq	%rcx, 0x10(%rsp)
   3dfeb:      	movq	%r14, 0x18(%rsp)
   3dff0:      	xorl	%edi, %edi
   3dff2:      	nopw	%cs:(%rax,%rax)
   3e000:      	movq	0x18(%rsp), %r14
   3e005:      	vmovupd	(%r14,%rdi,8), %ymm1
   3e00b:      	movq	0x8(%rsp), %r13
   3e010:      	vmovupd	(%r13,%rdi,8), %ymm2
   3e017:      	movq	-0x78(%rsp), %r8
   3e01c:      	vmovupd	(%r8,%rdi,8), %ymm4
   3e022:      	movq	-0x8(%rsp), %rbx
   3e027:      	vmovupd	(%rbx,%rdi,8), %ymm6
   3e02c:      	movq	-0x18(%rsp), %r11
   3e031:      	vmovupd	(%r11,%rdi,8), %ymm3
   3e037:      	movq	-0x28(%rsp), %rbp
   3e03c:      	vmovupd	(%rbp,%rdi,8), %ymm5
   3e042:      	movq	-0x60(%rsp), %rax
   3e047:      	vmovupd	(%rax,%rdi,8), %ymm9
   3e04c:      	movq	-0x68(%rsp), %rax
   3e051:      	vmovupd	(%rax,%rdi,8), %ymm10
   3e056:      	movq	-0x40(%rsp), %rsi
   3e05b:      	vaddpd	(%rsi,%rdi,8), %ymm1, %ymm7
   3e060:      	movq	0x10(%rsp), %r9
   3e065:      	vsubpd	(%r9,%rdi,8), %ymm2, %ymm11
   3e06b:      	vsubpd	%ymm11, %ymm7, %ymm0
   3e070:      	vfmadd213pd	%ymm0, %ymm8, %ymm2 # ymm2 = (ymm8 * ymm2) + ymm0
   3e075:      	movq	(%rsp), %r10
   3e079:      	vaddpd	(%r10,%rdi,8), %ymm4, %ymm14
   3e07f:      	movq	-0x10(%rsp), %r12
   3e084:      	vsubpd	(%r12,%rdi,8), %ymm6, %ymm13
   3e08a:      	vfmsub213pd	%ymm0, %ymm8, %ymm1 # ymm1 = (ymm8 * ymm1) - ymm0
   3e08f:      	vaddpd	%ymm13, %ymm14, %ymm0
   3e094:      	vfnmadd213pd	%ymm0, %ymm8, %ymm6 # ymm6 = -(ymm8 * ymm6) + ymm0
   3e099:      	vfmsub213pd	%ymm0, %ymm8, %ymm4 # ymm4 = (ymm8 * ymm4) - ymm0
   3e09e:      	vsubpd	%ymm6, %ymm2, %ymm0
   3e0a2:      	vfmadd213pd	%ymm0, %ymm8, %ymm14 # ymm14 = (ymm8 * ymm14) + ymm0
   3e0a7:      	vfmsub213pd	%ymm0, %ymm8, %ymm7 # ymm7 = (ymm8 * ymm7) - ymm0
   3e0ac:      	vmovupd	%ymm7, 0x30(%rsp)
   3e0b2:      	vaddpd	%ymm4, %ymm1, %ymm0
   3e0b6:      	vfmadd213pd	%ymm0, %ymm8, %ymm13 # ymm13 = (ymm8 * ymm13) + ymm0
   3e0bb:      	vfnmadd213pd	%ymm0, %ymm8, %ymm11 # ymm11 = -(ymm8 * ymm11) + ymm0
   3e0c0:      	vmovupd	%ymm11, 0x70(%rsp)
   3e0c6:      	movq	-0x20(%rsp), %r15
   3e0cb:      	vaddpd	(%r15,%rdi,8), %ymm3, %ymm11
   3e0d1:      	movq	-0x30(%rsp), %rdx
   3e0d6:      	vsubpd	(%rdx,%rdi,8), %ymm5, %ymm12
   3e0db:      	vsubpd	%ymm12, %ymm11, %ymm7
   3e0e0:      	vfmadd213pd	%ymm7, %ymm8, %ymm5 # ymm5 = (ymm8 * ymm5) + ymm7
   3e0e5:      	movq	-0x38(%rsp), %rcx
   3e0ea:      	vaddpd	(%rcx,%rdi,8), %ymm9, %ymm0
   3e0ef:      	movq	-0x48(%rsp), %rax
   3e0f4:      	vsubpd	(%rax,%rdi,8), %ymm10, %ymm15
   3e0f9:      	vfmsub213pd	%ymm7, %ymm8, %ymm3 # ymm3 = (ymm8 * ymm3) - ymm7
   3e0fe:      	vaddpd	%ymm0, %ymm15, %ymm7
   3e102:      	vfnmadd213pd	%ymm7, %ymm8, %ymm10 # ymm10 = -(ymm8 * ymm10) + ymm7
   3e107:      	vfmsub213pd	%ymm7, %ymm8, %ymm9 # ymm9 = (ymm8 * ymm9) - ymm7
   3e10c:      	vaddpd	%ymm5, %ymm10, %ymm7
   3e110:      	vfnmadd213pd	%ymm7, %ymm8, %ymm0 # ymm0 = -(ymm8 * ymm0) + ymm7
   3e115:      	vfmsub213pd	%ymm7, %ymm8, %ymm11 # ymm11 = (ymm8 * ymm11) - ymm7
   3e11a:      	vsubpd	%ymm9, %ymm3, %ymm7
   3e11f:      	vfnmadd213pd	%ymm7, %ymm8, %ymm15 # ymm15 = -(ymm8 * ymm15) + ymm7
   3e124:      	vfnmadd213pd	%ymm7, %ymm8, %ymm12 # ymm12 = -(ymm8 * ymm12) + ymm7
   3e129:      	vaddpd	%ymm0, %ymm14, %ymm7
   3e12d:      	vfnmadd213pd	%ymm7, %ymm8, %ymm5 # ymm5 = -(ymm8 * ymm5) + ymm7
   3e132:      	vfmsub213pd	%ymm7, %ymm8, %ymm2 # ymm2 = (ymm8 * ymm2) - ymm7
   3e137:      	vaddpd	%ymm15, %ymm13, %ymm7
   3e13c:      	vfnmadd213pd	%ymm7, %ymm8, %ymm3 # ymm3 = -(ymm8 * ymm3) + ymm7
   3e141:      	vfmsub213pd	%ymm7, %ymm8, %ymm1 # ymm1 = (ymm8 * ymm1) - ymm7
   3e146:      	vmovupd	%ymm1, 0x50(%rsp)
   3e14c:      	vaddpd	0x30(%rsp), %ymm11, %ymm7
   3e152:      	vfmadd213pd	%ymm7, %ymm8, %ymm10 # ymm10 = (ymm8 * ymm10) + ymm7
   3e157:      	vfnmadd213pd	%ymm7, %ymm8, %ymm6 # ymm6 = -(ymm8 * ymm6) + ymm7
   3e15c:      	vmovupd	0x70(%rsp), %ymm1
   3e162:      	vaddpd	%ymm1, %ymm12, %ymm7
   3e166:      	vfmadd213pd	%ymm7, %ymm8, %ymm9 # ymm9 = (ymm8 * ymm9) + ymm7
   3e16b:      	vfnmadd213pd	%ymm7, %ymm8, %ymm4 # ymm4 = -(ymm8 * ymm4) + ymm7
   3e170:      	vfmsub213pd	%ymm5, %ymm8, %ymm14 # ymm14 = (ymm8 * ymm14) - ymm5
   3e175:      	vmovupd	%ymm14, (%r14,%rdi,8)
   3e17b:      	vfmsub213pd	%ymm3, %ymm8, %ymm13 # ymm13 = (ymm8 * ymm13) - ymm3
   3e180:      	vmovupd	%ymm13, (%rsi,%rdi,8)
   3e185:      	vmovupd	0x30(%rsp), %ymm13
   3e18b:      	vfmsub213pd	%ymm10, %ymm8, %ymm13 # ymm13 = (ymm8 * ymm13) - ymm10
   3e190:      	vmovupd	%ymm10, (%r13,%rdi,8)
   3e197:      	vfmsub213pd	%ymm9, %ymm8, %ymm1 # ymm1 = (ymm8 * ymm1) - ymm9
   3e19c:      	vmovupd	%ymm9, (%r9,%rdi,8)
   3e1a2:      	vfmadd213pd	%ymm2, %ymm8, %ymm0 # ymm0 = (ymm8 * ymm0) + ymm2
   3e1a7:      	vmovupd	%ymm0, (%r8,%rdi,8)
   3e1ad:      	vmovupd	0x50(%rsp), %ymm0
   3e1b3:      	vfmadd213pd	%ymm0, %ymm8, %ymm15 # ymm15 = (ymm8 * ymm15) + ymm0
   3e1b8:      	vmovupd	%ymm15, (%r10,%rdi,8)
   3e1be:      	vfnmadd213pd	%ymm6, %ymm8, %ymm11 # ymm11 = -(ymm8 * ymm11) + ymm6
   3e1c3:      	vmovupd	%ymm6, (%rbx,%rdi,8)
   3e1c8:      	vfnmadd213pd	%ymm4, %ymm8, %ymm12 # ymm12 = -(ymm8 * ymm12) + ymm4
   3e1cd:      	vmovupd	%ymm4, (%r12,%rdi,8)
   3e1d3:      	vmovupd	%ymm5, (%r11,%rdi,8)
   3e1d9:      	vmovupd	%ymm3, (%r15,%rdi,8)
   3e1df:      	vmovupd	%ymm13, (%rbp,%rdi,8)
   3e1e5:      	vmovupd	%ymm1, (%rdx,%rdi,8)
   3e1ea:      	movq	-0x60(%rsp), %rdx
   3e1ef:      	vmovupd	%ymm2, (%rdx,%rdi,8)
   3e1f4:      	vmovupd	%ymm0, (%rcx,%rdi,8)
   3e1f9:      	movq	-0x68(%rsp), %rcx
   3e1fe:      	vmovupd	%ymm11, (%rcx,%rdi,8)
   3e203:      	vmovupd	%ymm12, (%rax,%rdi,8)
   3e208:      	addq	$0x4, %rdi
   3e20c:      	cmpq	-0x70(%rsp), %rdi
   3e211:      	jb	0x3e000 <hstep_g52_nat+0x170>
   3e217:      	movq	-0x50(%rsp), %rdx
   3e21c:      	addq	-0x58(%rsp), %rdx
   3e221:      	movq	0x20(%rsp), %rdi
   3e226:      	addq	%rdi, -0x48(%rsp)
   3e22b:      	addq	%rdi, -0x68(%rsp)
   3e230:      	movq	-0x38(%rsp), %rax
   3e235:      	addq	%rdi, %rax
   3e238:      	movq	-0x60(%rsp), %r11
   3e23d:      	addq	%rdi, %r11
   3e240:      	movq	-0x30(%rsp), %rbp
   3e245:      	addq	%rdi, %rbp
   3e248:      	movq	-0x28(%rsp), %r15
   3e24d:      	addq	%rdi, %r15
   3e250:      	movq	-0x20(%rsp), %r8
   3e255:      	addq	%rdi, %r8
   3e258:      	movq	-0x18(%rsp), %r12
   3e25d:      	addq	%rdi, %r12
   3e260:      	movq	-0x10(%rsp), %rbx
   3e265:      	addq	%rdi, %rbx
   3e268:      	movq	-0x8(%rsp), %r10
   3e26d:      	addq	%rdi, %r10
   3e270:      	movq	(%rsp), %r13
   3e274:      	addq	%rdi, %r13
   3e277:      	movq	-0x78(%rsp), %r9
   3e27c:      	addq	%rdi, %r9
   3e27f:      	movq	0x10(%rsp), %rcx
   3e284:      	addq	%rdi, %rcx
   3e287:      	movq	0x8(%rsp), %rsi
   3e28c:      	addq	%rdi, %rsi
   3e28f:      	movq	0x18(%rsp), %r14
   3e294:      	addq	%rdi, %r14
   3e297:      	addq	%rdi, -0x40(%rsp)
   3e29c:      	movq	%rdx, -0x50(%rsp)
   3e2a1:      	cmpq	0x28(%rsp), %rdx
   3e2a6:      	jb	0x3dfb0 <hstep_g52_nat+0x120>
   3e2ac:      	addq	$0x98, %rsp
   3e2b3:      	popq	%rbx
   3e2b4:      	popq	%r12
   3e2b6:      	popq	%r13
   3e2b8:      	popq	%r14
   3e2ba:      	popq	%r15
   3e2bc:      	popq	%rbp
   3e2bd:      	vzeroupper
   3e2c0:      	retq
   3e2c1:      	nopw	%cs:(%rax,%rax)

000000000003e2d0 <hfirst_tb8_balS>:
   3e2d0:      	vmovaps	(%rip), %ymm0           # 0x3e2d8 <hfirst_tb8_balS+0x8>
   3e2d8:      	testq	%rsi, %rsi
   3e2db:      	je	0x3e50a <hfirst_tb8_balS+0x23a>
   3e2e1:      	xorl	%eax, %eax
   3e2e3:      	vxorpd	%xmm1, %xmm1, %xmm1
   3e2e7:      	nopw	(%rax,%rax)
   3e2f0:      	vmovupd	(%rdi,%rax,8), %ymm2
   3e2f5:      	vmovupd	0x20(%rdi,%rax,8), %ymm4
   3e2fb:      	vmovupd	0x40(%rdi,%rax,8), %ymm5
   3e301:      	vmovupd	0x60(%rdi,%rax,8), %ymm6
   3e307:      	vmovddup	%ymm2, %ymm3            # ymm3 = ymm2[0,0,2,2]
   3e30b:      	vshufpd	$0xf, %ymm2, %ymm2, %ymm2 # ymm2 = ymm2[1,1,3,3]
   3e310:      	vsubpd	%ymm2, %ymm1, %ymm2
   3e314:      	vaddsubpd	%ymm2, %ymm3, %ymm2
   3e318:      	vpermpd	$0x44, %ymm2, %ymm3     # ymm3 = ymm2[0,1,0,1]
   3e31e:      	vsubpd	%ymm2, %ymm1, %ymm7
   3e322:      	vperm2f128	$0x31, %ymm7, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm7[2,3]
   3e328:      	vaddpd	%ymm2, %ymm3, %ymm3
   3e32c:      	vmovddup	%ymm4, %ymm2            # ymm2 = ymm4[0,0,2,2]
   3e330:      	vshufpd	$0xf, %ymm4, %ymm4, %ymm4 # ymm4 = ymm4[1,1,3,3]
   3e335:      	vsubpd	%ymm4, %ymm1, %ymm4
   3e339:      	vaddsubpd	%ymm4, %ymm2, %ymm2
   3e33d:      	vpermpd	$0x44, %ymm2, %ymm4     # ymm4 = ymm2[0,1,0,1]
   3e343:      	vsubpd	%ymm2, %ymm1, %ymm7
   3e347:      	vperm2f128	$0x31, %ymm7, %ymm2, %ymm2 # ymm2 = ymm2[2,3],ymm7[2,3]
   3e34d:      	vaddpd	%ymm2, %ymm4, %ymm2
   3e351:      	vmovddup	%ymm5, %ymm4            # ymm4 = ymm5[0,0,2,2]
   3e355:      	vshufpd	$0xf, %ymm5, %ymm5, %ymm5 # ymm5 = ymm5[1,1,3,3]
   3e35a:      	vsubpd	%ymm5, %ymm1, %ymm5
   3e35e:      	vaddsubpd	%ymm5, %ymm4, %ymm4
   3e362:      	vpermpd	$0x44, %ymm4, %ymm5     # ymm5 = ymm4[0,1,0,1]
   3e368:      	vsubpd	%ymm4, %ymm1, %ymm7
   3e36c:      	vperm2f128	$0x31, %ymm7, %ymm4, %ymm4 # ymm4 = ymm4[2,3],ymm7[2,3]
   3e372:      	vaddpd	%ymm4, %ymm5, %ymm5
   3e376:      	vmovddup	%ymm6, %ymm4            # ymm4 = ymm6[0,0,2,2]
   3e37a:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm6 # ymm6 = ymm6[1,1,3,3]
   3e37f:      	vsubpd	%ymm6, %ymm1, %ymm6
   3e383:      	vaddsubpd	%ymm6, %ymm4, %ymm4
   3e387:      	vpermpd	$0x44, %ymm4, %ymm6     # ymm6 = ymm4[0,1,0,1]
   3e38d:      	vsubpd	%ymm4, %ymm1, %ymm7
   3e391:      	vperm2f128	$0x31, %ymm7, %ymm4, %ymm4 # ymm4 = ymm4[2,3],ymm7[2,3]
   3e397:      	vaddpd	%ymm4, %ymm6, %ymm4
   3e39b:      	vmovupd	0x80(%rdi,%rax,8), %ymm6
   3e3a4:      	vmovddup	%ymm6, %ymm7            # ymm7 = ymm6[0,0,2,2]
   3e3a8:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm6 # ymm6 = ymm6[1,1,3,3]
   3e3ad:      	vsubpd	%ymm6, %ymm1, %ymm6
   3e3b1:      	vaddsubpd	%ymm6, %ymm7, %ymm6
   3e3b5:      	vpermpd	$0x44, %ymm6, %ymm7     # ymm7 = ymm6[0,1,0,1]
   3e3bb:      	vsubpd	%ymm6, %ymm1, %ymm8
   3e3bf:      	vperm2f128	$0x31, %ymm8, %ymm6, %ymm6 # ymm6 = ymm6[2,3],ymm8[2,3]
   3e3c5:      	vaddpd	%ymm6, %ymm7, %ymm8
   3e3c9:      	vmovupd	0xa0(%rdi,%rax,8), %ymm6
   3e3d2:      	vmovddup	%ymm6, %ymm7            # ymm7 = ymm6[0,0,2,2]
   3e3d6:      	vshufpd	$0xf, %ymm6, %ymm6, %ymm6 # ymm6 = ymm6[1,1,3,3]
   3e3db:      	vsubpd	%ymm6, %ymm1, %ymm6
   3e3df:      	vaddsubpd	%ymm6, %ymm7, %ymm6
   3e3e3:      	vpermpd	$0x44, %ymm6, %ymm7     # ymm7 = ymm6[0,1,0,1]
   3e3e9:      	vsubpd	%ymm6, %ymm1, %ymm9
   3e3ed:      	vperm2f128	$0x31, %ymm9, %ymm6, %ymm6 # ymm6 = ymm6[2,3],ymm9[2,3]
   3e3f3:      	vaddpd	%ymm6, %ymm7, %ymm6
   3e3f7:      	vmovupd	0xc0(%rdi,%rax,8), %ymm7
   3e400:      	vmovddup	%ymm7, %ymm9            # ymm9 = ymm7[0,0,2,2]
   3e404:      	vshufpd	$0xf, %ymm7, %ymm7, %ymm7 # ymm7 = ymm7[1,1,3,3]
   3e409:      	vsubpd	%ymm7, %ymm1, %ymm7
   3e40d:      	vaddsubpd	%ymm7, %ymm9, %ymm7
   3e411:      	vpermpd	$0x44, %ymm7, %ymm9     # ymm9 = ymm7[0,1,0,1]
   3e417:      	vsubpd	%ymm7, %ymm1, %ymm10
   3e41b:      	vperm2f128	$0x31, %ymm10, %ymm7, %ymm7 # ymm7 = ymm7[2,3],ymm10[2,3]
   3e421:      	vaddpd	%ymm7, %ymm9, %ymm9
   3e425:      	vmovupd	0xe0(%rdi,%rax,8), %ymm7
   3e42e:      	vmovddup	%ymm7, %ymm10           # ymm10 = ymm7[0,0,2,2]
   3e432:      	vshufpd	$0xf, %ymm7, %ymm7, %ymm7 # ymm7 = ymm7[1,1,3,3]
   3e437:      	vsubpd	%ymm7, %ymm1, %ymm7
   3e43b:      	vaddsubpd	%ymm7, %ymm10, %ymm7
   3e43f:      	vpermpd	$0x44, %ymm7, %ymm10    # ymm10 = ymm7[0,1,0,1]
   3e445:      	vsubpd	%ymm7, %ymm1, %ymm11
   3e449:      	vperm2f128	$0x31, %ymm11, %ymm7, %ymm7 # ymm7 = ymm7[2,3],ymm11[2,3]
   3e44f:      	vaddpd	%ymm7, %ymm10, %ymm7
   3e453:      	vsubpd	%ymm2, %ymm3, %ymm10
   3e457:      	vfmadd213pd	%ymm3, %ymm0, %ymm2 # ymm2 = (ymm0 * ymm2) + ymm3
   3e45c:      	vsubpd	%ymm4, %ymm5, %ymm3
   3e460:      	vfmadd213pd	%ymm5, %ymm0, %ymm4 # ymm4 = (ymm0 * ymm4) + ymm5
   3e465:      	vsubpd	%ymm6, %ymm8, %ymm5
   3e469:      	vfmadd213pd	%ymm8, %ymm0, %ymm6 # ymm6 = (ymm0 * ymm6) + ymm8
   3e46e:      	vsubpd	%ymm7, %ymm9, %ymm8
   3e472:      	vfmadd213pd	%ymm9, %ymm0, %ymm7 # ymm7 = (ymm0 * ymm7) + ymm9
   3e477:      	vsubpd	%ymm4, %ymm2, %ymm9
   3e47b:      	vfmadd213pd	%ymm2, %ymm0, %ymm4 # ymm4 = (ymm0 * ymm4) + ymm2
   3e480:      	vsubpd	%ymm3, %ymm10, %ymm2
   3e484:      	vfmadd213pd	%ymm10, %ymm0, %ymm3 # ymm3 = (ymm0 * ymm3) + ymm10
   3e489:      	vsubpd	%ymm7, %ymm6, %ymm10
   3e48d:      	vfmadd213pd	%ymm6, %ymm0, %ymm7 # ymm7 = (ymm0 * ymm7) + ymm6
   3e492:      	vsubpd	%ymm8, %ymm5, %ymm6
   3e497:      	vfmadd213pd	%ymm5, %ymm0, %ymm8 # ymm8 = (ymm0 * ymm8) + ymm5
   3e49c:      	vsubpd	%ymm7, %ymm4, %ymm5
   3e4a0:      	vfmadd213pd	%ymm4, %ymm0, %ymm7 # ymm7 = (ymm0 * ymm7) + ymm4
   3e4a5:      	vsubpd	%ymm8, %ymm3, %ymm4
   3e4aa:      	vfmadd213pd	%ymm3, %ymm0, %ymm8 # ymm8 = (ymm0 * ymm8) + ymm3
   3e4af:      	vsubpd	%ymm10, %ymm9, %ymm3
   3e4b4:      	vfmadd213pd	%ymm9, %ymm0, %ymm10 # ymm10 = (ymm0 * ymm10) + ymm9
   3e4b9:      	vsubpd	%ymm6, %ymm2, %ymm9
   3e4bd:      	vfmadd213pd	%ymm2, %ymm0, %ymm6 # ymm6 = (ymm0 * ymm6) + ymm2
   3e4c2:      	vmovupd	%ymm7, (%rdi,%rax,8)
   3e4c7:      	vmovupd	%ymm8, 0x20(%rdi,%rax,8)
   3e4cd:      	vmovupd	%ymm10, 0x40(%rdi,%rax,8)
   3e4d3:      	vmovupd	%ymm6, 0x60(%rdi,%rax,8)
   3e4d9:      	vmovupd	%ymm5, 0x80(%rdi,%rax,8)
   3e4e2:      	vmovupd	%ymm4, 0xa0(%rdi,%rax,8)
   3e4eb:      	vmovupd	%ymm3, 0xc0(%rdi,%rax,8)
   3e4f4:      	vmovupd	%ymm9, 0xe0(%rdi,%rax,8)
   3e4fd:      	addq	$0x20, %rax
   3e501:      	cmpq	%rsi, %rax
   3e504:      	jb	0x3e2f0 <hfirst_tb8_balS+0x20>
   3e50a:      	vzeroupper
   3e50d:      	retq
   3e50e:      	nop

000000000003e510 <hstep_tb8_balS>:
   3e510:      	pushq	%r15
   3e512:      	pushq	%r14
   3e514:      	pushq	%r13
   3e516:      	pushq	%r12
   3e518:      	pushq	%rbx
   3e519:      	vmovaps	(%rip), %ymm0           # 0x3e521 <hstep_tb8_balS+0x11>
   3e521:      	testq	%rsi, %rsi
   3e524:      	je	0x3e68e <hstep_tb8_balS+0x17e>
   3e52a:      	testq	%rdx, %rdx
   3e52d:      	je	0x3e68e <hstep_tb8_balS+0x17e>
   3e533:      	leaq	(,%rdx,8), %rax
   3e53b:      	movq	%rdx, %rcx
   3e53e:      	shlq	$0x4, %rcx
   3e542:      	leaq	(%rdx,%rdx,2), %r8
   3e546:      	movq	%rdx, %r9
   3e549:      	shlq	$0x5, %r9
   3e54d:      	leaq	(%rdx,%rdx,4), %r14
   3e551:      	leaq	(%rdi,%r8,8), %r10
   3e555:      	shlq	$0x4, %r8
   3e559:      	imulq	$0x38, %rdx, %r11
   3e55d:      	addq	%rdi, %r11
   3e560:      	movq	%rdx, %rbx
   3e563:      	shlq	$0x6, %rbx
   3e567:      	addq	%rdi, %r8
   3e56a:      	leaq	(%rdi,%r14,8), %r14
   3e56e:      	addq	%rdi, %r9
   3e571:      	addq	%rdi, %rcx
   3e574:      	leaq	(%rdi,%rax), %r15
   3e578:      	xorl	%r12d, %r12d
   3e57b:      	nopl	(%rax,%rax)
   3e580:      	xorl	%r13d, %r13d
   3e583:      	nopw	%cs:(%rax,%rax)
   3e590:      	vmovupd	(%rdi,%r13,8), %ymm2
   3e596:      	vmovupd	(%r15,%r13,8), %ymm3
   3e59c:      	vmovupd	(%rcx,%r13,8), %ymm4
   3e5a2:      	vmovupd	(%r10,%r13,8), %ymm5
   3e5a8:      	vmovupd	(%r9,%r13,8), %ymm6
   3e5ae:      	vmovupd	(%r14,%r13,8), %ymm7
   3e5b4:      	vmovupd	(%r8,%r13,8), %ymm8
   3e5ba:      	vmovupd	(%r11,%r13,8), %ymm1
   3e5c0:      	vsubpd	%ymm3, %ymm2, %ymm9
   3e5c4:      	vfmadd213pd	%ymm2, %ymm0, %ymm3 # ymm3 = (ymm0 * ymm3) + ymm2
   3e5c9:      	vsubpd	%ymm5, %ymm4, %ymm2
   3e5cd:      	vfmadd213pd	%ymm4, %ymm0, %ymm5 # ymm5 = (ymm0 * ymm5) + ymm4
   3e5d2:      	vsubpd	%ymm7, %ymm6, %ymm4
   3e5d6:      	vfmadd213pd	%ymm6, %ymm0, %ymm7 # ymm7 = (ymm0 * ymm7) + ymm6
   3e5db:      	vsubpd	%ymm1, %ymm8, %ymm6
   3e5df:      	vfmadd213pd	%ymm8, %ymm0, %ymm1 # ymm1 = (ymm0 * ymm1) + ymm8
   3e5e4:      	vsubpd	%ymm5, %ymm3, %ymm8
   3e5e8:      	vfmadd213pd	%ymm3, %ymm0, %ymm5 # ymm5 = (ymm0 * ymm5) + ymm3
   3e5ed:      	vsubpd	%ymm2, %ymm9, %ymm3
   3e5f1:      	vfmadd213pd	%ymm9, %ymm0, %ymm2 # ymm2 = (ymm0 * ymm2) + ymm9
   3e5f6:      	vsubpd	%ymm1, %ymm7, %ymm9
   3e5fa:      	vfmadd213pd	%ymm7, %ymm0, %ymm1 # ymm1 = (ymm0 * ymm1) + ymm7
   3e5ff:      	vsubpd	%ymm6, %ymm4, %ymm7
   3e603:      	vfmadd213pd	%ymm4, %ymm0, %ymm6 # ymm6 = (ymm0 * ymm6) + ymm4
   3e608:      	vsubpd	%ymm1, %ymm5, %ymm4
   3e60c:      	vfmadd213pd	%ymm5, %ymm0, %ymm1 # ymm1 = (ymm0 * ymm1) + ymm5
   3e611:      	vsubpd	%ymm6, %ymm2, %ymm5
   3e615:      	vfmadd213pd	%ymm2, %ymm0, %ymm6 # ymm6 = (ymm0 * ymm6) + ymm2
   3e61a:      	vsubpd	%ymm9, %ymm8, %ymm2
   3e61f:      	vfmadd213pd	%ymm8, %ymm0, %ymm9 # ymm9 = (ymm0 * ymm9) + ymm8
   3e624:      	vsubpd	%ymm7, %ymm3, %ymm8
   3e628:      	vfmadd213pd	%ymm3, %ymm0, %ymm7 # ymm7 = (ymm0 * ymm7) + ymm3
   3e62d:      	vmovupd	%ymm1, (%rdi,%r13,8)
   3e633:      	vmovupd	%ymm6, (%r15,%r13,8)
   3e639:      	vmovupd	%ymm9, (%rcx,%r13,8)
   3e63f:      	vmovupd	%ymm7, (%r10,%r13,8)
   3e645:      	vmovupd	%ymm4, (%r9,%r13,8)
   3e64b:      	vmovupd	%ymm5, (%r14,%r13,8)
   3e651:      	vmovupd	%ymm2, (%r8,%r13,8)
   3e657:      	vmovupd	%ymm8, (%r11,%r13,8)
   3e65d:      	addq	$0x4, %r13
   3e661:      	cmpq	%rdx, %r13
   3e664:      	jb	0x3e590 <hstep_tb8_balS+0x80>
   3e66a:      	addq	%rax, %r12
   3e66d:      	addq	%rbx, %r11
   3e670:      	addq	%rbx, %r8
   3e673:      	addq	%rbx, %r14
   3e676:      	addq	%rbx, %r9
   3e679:      	addq	%rbx, %r10
   3e67c:      	addq	%rbx, %rcx
   3e67f:      	addq	%rbx, %rdi
   3e682:      	addq	%rbx, %r15
   3e685:      	cmpq	%rsi, %r12
   3e688:      	jb	0x3e580 <hstep_tb8_balS+0x70>
   3e68e:      	popq	%rbx
   3e68f:      	popq	%r12
   3e691:      	popq	%r13
   3e693:      	popq	%r14
   3e695:      	popq	%r15
   3e697:      	vzeroupper
   3e69a:      	retq
   3e69b:      	nopl	(%rax,%rax)


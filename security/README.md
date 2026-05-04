# Security — OpenTitan RoT

Discrete OpenTitan chip on SPI to the Strix Halo SoC, providing TPM 2.0 capabilities.

## Sourcing

Commercial OpenTitan silicon is available via:
- **zeroRISC** early access program — https://zerorisc.com/
- **Nuvoton** discrete OpenTitan SKU

## Wiring

- SPI (clk + MOSI + MISO + CS) from SoC
- INT pin to EC for tamper / wake
- Reset from EC
- 3.3 V supply from main rail

## TPM 2.0 use cases

- Measured boot of coreboot + edk2
- LUKS root key sealing
- SSH key storage via `tpm2-pkcs11`

## Provisioning

```bash
# After first power-on
sudo tpm2_createek -G rsa -c ek_handle.ctx
sudo tpm2_certifycreation -c ek_handle.ctx ...
```

## Status

Hardware design pending Strix Halo motherboard schematic.
